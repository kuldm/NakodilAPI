from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

# from db import engine
from infrastructure.postgres.models.models import Event, EventSeat, Location, Seat
from infrastructure.postgres.db_manager import PostgresClient


async def add_event_data_to_db(postgres: PostgresClient) -> None:
    async with postgres.session() as db:
        session = db.session

        count = await session.scalar(select(func.count()).select_from(Location))
        if count:
            print("Тестовые данные уже существуют")
            return

        location = Location(
            name="Центральный зал",
            city="Москва",
            address="Тверская улица, 1",
        )
        session.add(location)
        await session.flush()

        seats = [
            Seat(
                location_id=location.id,
                sector="Основной сектор",
                row=row,
                number=number,
                x=number * 50,
                y=row * 50,
            )
            for row in range(1, 6)
            for number in range(1, 11)
        ]
        session.add_all(seats)
        await session.flush()

        event = Event(
            organizer_id=1,
            location_id=location.id,
            title="Python Конференция",
            description="Тестовое мероприятие для домашнего задания",
            category="конференция",
            starts_at=datetime.now(timezone.utc) + timedelta(days=30),
            base_price=5000,
        )
        session.add(event)
        await session.flush()

        session.add_all(
            EventSeat(event_id=event.id, seat_id=seat.id, price=event.base_price)
            for seat in seats
        )

        await db.commit()

    print("Тестовые данные созданы")