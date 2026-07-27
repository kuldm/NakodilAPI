import pytest
from httpx import AsyncClient, ASGITransport

import services.reports as reports_module

# from config import settings
from config import AppConfig
from main import app
from services.reports import jobs


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode() -> None:
    assert AppConfig.mode == "TEST"


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
def reset_jobs():
    jobs.clear()
    reports_module.next_job_id = 1
    yield
    jobs.clear()
    reports_module.next_job_id = 1
