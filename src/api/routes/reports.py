from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path

from schemas.reports import JobStatusResponse, JobResult
from services.reports import JobService

router = APIRouter(prefix="/reports", route_class=DishkaRoute, tags=["Отчёты"])


@router.post(
    "/{user_id}",
    summary="Получение отчёта пользователя",
    description="<h3>Этот метод возвращает отчёт пользователя<h3>",
    response_model=JobStatusResponse,
)
async def get_user_report(
    service: FromDishka[JobService],
    user_id: int = Path(example=1, description="ID задачи", ge=1, le=208),  # noqa
):
    return await service.create_job(user_id)


@router.get(
    "/jobs/{job_id}",
    summary="Получение статуса задачи",
    description="<h3>Этот метод возвращает статус задачи<h3>",
    response_model=JobResult,
)
async def get_status_job(
    service: FromDishka[JobService],
    job_id: int = Path(example=1, description="ID задачи", ge=1),  # noqa
):
    return await service.get_job(job_id)
