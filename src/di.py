from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide

from config import settings
from db import async_session_maker
from infrustructure.api_connectors.internal.payment import PaymentConnector
from infrustructure.api_connectors.internal.protection import ProtectionConnector
from services.events import EventsService
from utils.db_manager import DBManager


class AppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def db(self) -> AsyncIterator[DBManager]:
        async with DBManager(session_factory=async_session_maker) as db:
            yield db

    @provide(scope=Scope.APP)
    def payment_connector(self) -> PaymentConnector:
        return PaymentConnector(
            base_url=settings.PAYMENT_API_URL, timeout=settings.PAYMENT_TIMEOUT
        )

    @provide(scope=Scope.APP)
    def protection_connector(self) -> ProtectionConnector:
        return ProtectionConnector(
            base_url=settings.PROTECTION_API_URL, timeout=settings.PROTECTION_TIMEOUT
        )

    @provide(scope=Scope.REQUEST)
    def events_service(
        self,
        db: DBManager,
        payment_connector: PaymentConnector,
        protection_connector: ProtectionConnector,
    ) -> EventsService:
        return EventsService(
            db=db,
            payment_connector=payment_connector,
            protection_connector=protection_connector,
        )
