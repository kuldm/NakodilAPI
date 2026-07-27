from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
    AsyncSession,
)

from config import PostgresConfig
from infrastructure.postgres.repositories.bookings import BookingsRepository
from infrastructure.postgres.repositories.events import EventsRepository
from infrastructure.postgres.repositories.organizers import OrganizersRepository
from infrastructure.postgres.repositories.seats import (
    SeatsRepository,
    EventsSeatsRepository,
)


class PostgresClient:
    def __init__(self, config: PostgresConfig) -> None:
        self._engine: AsyncEngine = create_async_engine(
            config.url,
            echo=config.echo,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_pre_ping=True,
        )

        self._session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncIterator["DatabaseManager"]:
        async with self._session_maker() as session:
            db = DatabaseManager(session, self._session_maker)
            try:
                yield db
            except Exception:
                await db.rollback()
                raise

    async def close(self) -> None:
        await self._engine.dispose()


class DatabaseManager:
    def __init__(
        self, session: AsyncSession, session_maker: async_sessionmaker
    ) -> None:
        self.session = session
        self.session_maker = session_maker

    @asynccontextmanager
    async def transaction(self):
        async with self.session_maker() as new_session:
            db = DatabaseManager(new_session, self.session_maker)
            try:
                yield db
                await db.commit()
            except:
                await db.rollback()
                raise

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @property
    def bookings(self) -> BookingsRepository:
        return BookingsRepository(self.session)

    @property
    def events(self) -> EventsRepository:
        return EventsRepository(self.session)

    @property
    def organizers(self) -> OrganizersRepository:
        return OrganizersRepository(self.session)

    @property
    def seats(self) -> SeatsRepository:
        return SeatsRepository(self.session)

    @property
    def events_seats(self) -> EventsSeatsRepository:
        return EventsSeatsRepository(self.session)
