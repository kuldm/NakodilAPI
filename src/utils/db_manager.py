from contextlib import asynccontextmanager

from repositories.bookings import BookingsRepository
from repositories.events import EventsRepository
from repositories.organizers import OrganizersRepository
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
        self.organizers = OrganizersRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @asynccontextmanager
    async def transaction(self):
        session = self.session_factory()

        db = DBManager(self.session_factory)
        db.session = session

        db.events = EventsRepository(session)
        db.bookings = BookingsRepository(session)
        db.seats = SeatsRepository(session)
        db.events_seats = EventsSeatsRepository(session)
        db.organizers = OrganizersRepository(session)

        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        finally:
            await session.close()
