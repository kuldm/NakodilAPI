from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.fastapi import FastapiProvider

# from config import settings
from config import (
    Settings,
    PostgresConfig,
    ReportConfig,
    BookingConfig,
    AppConfig,
    ConnectorsConfig,
)

# from db import async_session_maker
from infrastructure.api_connectors.internal.payment import PaymentConnector
from infrastructure.api_connectors.internal.protection import ProtectionConnector
from services.events import EventsService
from services.organizers import OrganizersService
from infrastructure.postgres.db_manager import PostgresClient, DatabaseManager


class ConfigProvider(Provider):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._settings = settings

    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return self._settings

    @provide(scope=Scope.APP)
    def get_postgres_config(self, settings: Settings) -> PostgresConfig:
        return settings.postgres

    @provide(scope=Scope.APP)
    def get_report_config(self, settings: Settings) -> ReportConfig:
        return settings.report

    @provide(scope=Scope.APP)
    def get_booking_config(self, settings: Settings) -> BookingConfig:
        return settings.booking

    @provide(scope=Scope.APP)
    def get_app_config(self, settings: Settings) -> AppConfig:
        return settings.app

    @provide(scope=Scope.APP)
    def get_connectors_config(self, settings: Settings) -> ConnectorsConfig:
        return settings.connectors


class PostgresProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_postgres(
        self,
        config: PostgresConfig,
    ) -> AsyncIterator[PostgresClient]:
        postgres = PostgresClient(config)

        yield postgres

        await postgres.close()

    @provide(scope=Scope.REQUEST)
    async def get_db(
        self,
        postgres: PostgresClient,
    ) -> AsyncIterator[DatabaseManager]:
        async with postgres.session() as db:
            yield db


class AppProvider(Provider):
    # @provide(scope=Scope.REQUEST)
    # async def db(self) -> AsyncIterator[DBManager]:
    #     async with DBManager(session_factory=async_session_maker) as db:
    #         yield db

    @provide(scope=Scope.APP)
    async def payment_connector(
        self,
        config: ConnectorsConfig,
    ) -> AsyncIterator[PaymentConnector]:
        payment_config = config.payment
        connector = PaymentConnector(
            base_url=payment_config.base_url, timeout=payment_config.timeout
        )

        yield connector

        await connector._close_client()

    @provide(scope=Scope.APP)
    async def protection_connector(
        self,
        config: ConnectorsConfig,
    ) -> AsyncIterator[ProtectionConnector]:
        protection_config = config.protection
        connector = ProtectionConnector(
            base_url=protection_config.base_url, timeout=protection_config.timeout
        )

        yield connector

        await connector._close_client()

    @provide(scope=Scope.REQUEST)
    def events_service(
        self,
        db: DatabaseManager,
        payment_connector: PaymentConnector,
        protection_connector: ProtectionConnector,
    ) -> EventsService:
        return EventsService(
            db=db,
            payment_connector=payment_connector,
            protection_connector=protection_connector,
        )

    @provide(scope=Scope.REQUEST)
    def organizers_service(
        self,
        db: DatabaseManager,
    ) -> OrganizersService:
        return OrganizersService(
            db=db,
        )


def create_container(settings: Settings):
    return make_async_container(
        ConfigProvider(settings),
        PostgresProvider(),
        AppProvider(),
        FastapiProvider(),
    )
