from repositories.events import EventsRepository
from repositories.bookings import BookingsRepository
from repositories.seats import SeatsRepository, EventsSeatsRepository


class DBManager:
    """
    Асинхронный контекстный менеджер для работы с базой данных
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.events = EventsRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.seats = SeatsRepository(self.session)
        self.events_seats = EventsSeatsRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
