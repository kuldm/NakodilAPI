from fastapi import APIRouter, Path

from exceptions import (
    JobNotFoundException,
    JobNotFoundHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from schemas.reports import JobStatusResponse, JobResult
from services.reports import JobService

router = APIRouter(prefix="/reports", tags=["Отчёты"])


@router.post(
    "/{user_id}",
    summary="Получение отчёта пользователя",
    description="<h3>Этот метод возвращает отчёт пользователя<h3>",
    response_model=JobStatusResponse,
)
async def get_user_report(
    user_id: int = Path(example=1, description="ID задачи", ge=1, le=208),
):
    try:
        return await JobService().create_job(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.get(
    "/jobs/{job_id}",
    summary="Получение статуса задачи",
    description="<h3>Этот метод возвращает статус задачи<h3>",
    response_model=JobResult,
)
async def get_status_job(job_id: int = Path(example=1, description="ID задачи", ge=1)):
    try:
        return await JobService().get_job(job_id)
    except JobNotFoundException:
        raise JobNotFoundHTTPException
