import logging
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from fastapi import FastAPI

from services.add_event_data import add_event_data_to_db
from infrastructure.postgres.db_manager import PostgresClient

logger = logging.getLogger(__name__)


def create_lifespan(container: AsyncContainer):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        postgres = await container.get(PostgresClient)
        await add_event_data_to_db(postgres)
        yield
        await app.state.dishka_container.close()

    return lifespan
