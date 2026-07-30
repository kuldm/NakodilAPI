import asyncio
import time

from infrastructure.postgres.db_manager import PostgresClient
from schemas.events import EventViews
from src.config import settings


class EventViewsWorker:
    def __init__(self, postgres: PostgresClient):
        self._postgres = postgres
        self._queue: asyncio.Queue[int] = asyncio.Queue()
        self._aggregates: dict[int, int] = {}  # event_id -> сколько просмотров
        self._pending: int = 0  # сколько сырых событий с прошлого flush
        self._worker_task: asyncio.Task | None = None

    def start(self) -> None:
        # запускается при старте приложения и запускается цикл _run
        self._worker_task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        # Отправляем запрос на отмену таски
        self._worker_task.cancel()
        try:
            # Дожидаемся завершения задачи и блока finally в run
            await self._worker_task
        except asyncio.CancelledError:
            pass

    # В очередь помещается только id мероприятия в список
    async def add_event_view(self, event_id: int) -> None:
        await self._queue.put(event_id)  # только id, без ORM

    async def _run(self) -> None:
        # задаём время следующей отправки данных
        next_flush = time.monotonic() + settings.event_views.flush_interval
        try:
            # Бесконечный цикл
            while True:
                try:
                    # берём из очереди id до тех пор пока не истечёт таймаут, после истечения выбрасывает ошибку
                    event_id = await asyncio.wait_for(
                        self._queue.get(), timeout=max(next_flush - time.monotonic(), 0)
                    )
                # как истечёт таймаут то выбрасываем ошибку и записывает агрегированные данные если они есть
                except asyncio.TimeoutError:
                    # раз в 5(установлено в .env) сек если есть накопленное записываем данные
                    if self._aggregates:
                        await self._flush()
                    # Устанавливаем время следующе загрузки данных
                    next_flush = time.monotonic() + settings.event_views.flush_interval
                    continue

                # агрегируем данные в памяти
                self._aggregates[event_id] = self._aggregates.get(event_id, 0) + 1
                # увеличиваем счётчик количества просмотров
                self._pending += 1
                # Когда количство просмотров становится 10 или больше установил в .env то записываем данные
                if self._pending >= settings.event_views.batch_size:
                    next_flush = time.monotonic() + settings.event_views.flush_interval
                    await self._flush()
        finally:
            # После команды stop срабатывает этот блок и мы отправляем данные которые не успели записаться в базу
            self._drain_queue()
            await self._flush()

    def _drain_queue(self) -> None:
        while not self._queue.empty():
            # Получаем элемент из очереди без ожидания
            event_id = self._queue.get_nowait()
            self._aggregates[event_id] = self._aggregates.get(event_id, 0) + 1

    async def _flush(self) -> None:
        if not self._aggregates:
            return
        # записываем данные по схеме
        batch = [
            EventViews(event_id=e_id, views_count=v_count)
            for e_id, v_count in self._aggregates.items()
        ]

        # Отправляем запрос в базу на запись
        async with self._postgres.session() as db:
            await db.event_views.update_event_views_bulk(batch)
            await db.commit()
        # Очищаем переменные
        self._aggregates.clear()
        self._pending = 0


