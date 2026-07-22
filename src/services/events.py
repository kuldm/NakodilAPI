import asyncio
from datetime import datetime, timedelta, timezone

# from config import settings
from config import settings
from exceptions import SeatsConflictException
from infrastructure.api_connectors.schemas import (
    PaymentCalculateItemData,
    ProtectionCalculateItemData,
)
from infrastructure.postgres.models.models import EventSeat, SeatStatus
from schemas.bookings import BookingCreate, BookingAdd, BookingPATCH, CheckoutBooking
from schemas.events import EventRead
from schemas.schemas import CheckoutResponse
from schemas.seats import EventSeatRead
from services.base import BaseService


class EventsService(BaseService):
    async def get_all_events(self) -> list[EventRead]:
        return await self.db.events.get_all()

    async def get_event_by_id(self, event_id: int) -> EventRead:
        return await self.db.events.get_one_or_none(id=event_id)

    async def get_event_seats(self, event_id: int) -> list[EventSeatRead]:
        return await self.db.events_seats.get_relation_seat_and_event_seats_by_event_id(
            event_id=event_id
        )

    async def prepare_checkout(
        self, user_id: int, event_id: int, payload: BookingCreate
    ) -> CheckoutResponse:
        # 1) Блокируем выбранные места
        seats = await self.db.events_seats.lock_for_reserve(
            event_id=event_id, seat_ids=payload.seat_ids
        )

        # 2) Конфликт → 409
        now = datetime.now(timezone.utc)
        if any(not self._is_free(seat, now) for seat in seats):
            raise SeatsConflictException

        reserved_until = now + timedelta(minutes=settings.booking.reservation_minutes)
        amount = sum(seat.price for seat in seats)

        # 3 Создаём бронь
        booking = await self.db.bookings.add(
            BookingAdd(
                event_id=event_id,
                user_id=user_id,
                amount=amount,
                payment_commission=0,
                protection_price=0,
                with_protection=False,
                reserved_until=reserved_until,
            )
        )

        # 4 Переводим места в reserved
        await self.db.events_seats.mark_reserved(
            seat_ids=[seat.id for seat in seats],
            booking_id=booking.id,
            reserved_until=reserved_until,
        )

        event = await self.get_event_by_id(event_id)

        # 5 Обращаемся к апи оплаты
        payment_task = asyncio.create_task(
            self.payment_connector.payment_calculate(
                PaymentCalculateItemData(
                    booking_id=booking.id, amount=booking.amount, currency="RUB"
                ),
            )
        )

        protection_payload = ProtectionCalculateItemData(
            booking_id=booking.id,
            ticket_amount=booking.amount,
            event_category=event.category,
            event_starts_at=str(event.starts_at),
        )

        # 6 Обращаемся к апи страховки
        protection_task = asyncio.create_task(
            self.protection_connector.protection_calculate(protection_payload)
        )
        # ожидаем результат оплаты
        payment = await payment_task

        # Пробуем дождать результата страховки, если не выполнится быстрее 3 секунд то выбрасываем ошибку
        try:
            protection = await asyncio.wait_for(protection_task, timeout=3)
        except TimeoutError as ex:
            print(f"Protection calculation error: {type(ex).__name__}: {ex}")
            protection = None

        # Добавляем в таблицу заказов полученные данные от сервиса оплаты и страховки
        booking = await self.db.bookings.edit(
            BookingPATCH(
                payment_commission=payment.commission,
                protection_price=(protection.price if protection else None),
                with_protection=(protection.available if protection else False),
            ),
            exclude_unset=True,
            id=booking.id,
        )
        await self.db.commit()

        booking = await self.db.bookings.get_one_or_none(id=booking.id)
        booking = CheckoutBooking(
            id=booking.id,
            event_title=event.title,
            starts_at=event.starts_at,
            seats=[
                {
                    "id": seat.id,
                    "seat_id": seat.seat_id,
                    "price": seat.price,
                }
                for seat in seats
            ],
            base_amount=booking.amount,
            payment_commission=booking.payment_commission,
            protection_price=booking.protection_price,
            with_protection=booking.with_protection,
            reserved_until=booking.reserved_until,
        )
        checkout_booking = CheckoutResponse(
            booking=booking,
            payment=payment,
            protection=protection,
        )
        return checkout_booking

    @classmethod
    def _is_free(cls, event_seat: EventSeat, now: datetime) -> bool:
        if event_seat.status == SeatStatus.available:
            return True
        if (
            event_seat.status == SeatStatus.reserved
            and event_seat.reserved_until is not None
            and event_seat.reserved_until < now
        ):
            return True
        return False

    # # НЕ используется но в перспеткиве дописать чтобы всё равно данные по страховке добавлялись в базу
    # async def _persist_protection_later(
    #     self,
    #     booking_id: int,
    #     payload: ProtectionCalculateItemData,
    #     first_task: asyncio.Task | None = None,
    # ) -> None:
    #     protection = None
    #
    #     # 1) дождаться первого конкурентного запроса
    #     if first_task is not None:
    #         try:
    #             protection = await first_task
    #         except Exception:
    #             protection = None
    #
    #     # 2) пока не получили валидный ответ — ретраим
    #     attempt = 0
    #     while protection is None:
    #         attempt += 1
    #         try:
    #             protection = await self.protection_connector.protection_calculate(
    #                 payload
    #             )
    #         except httpx.HTTPError:
    #             delay = 2 ** (attempt - 1)
    #             jitter = random.uniform(0.1, 0.5)
    #             await asyncio.sleep(delay + jitter)
    #
    #     async with self.postgres.session() as db:
    #         await db.bookings.edit(
    #             BookingPATCH(
    #                 protection_price=protection.price,
    #                 with_protection=protection.available,
    #             ),
    #             exclude_unset=True,
    #             id=booking_id,
    #         )
    #         await db.commit()
