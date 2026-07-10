import asyncio
from concurrent.futures import ThreadPoolExecutor

import httpx

from config import settings
from exceptions import JobNotFoundException, UserNotFoundException
from services.legacy_client import get_user_todos_sync
from schemas.reports import JobResult, JobStatusResponse, User, Job, Todo
from services.base import BaseService


class ReportService(BaseService):
    async def get_formated_user_todos_data(self, user_id: int) -> Todo:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future = executor.submit(get_user_todos_sync, user_id)
            todos = await asyncio.wrap_future(future)
        if todos:
            raw_todos = todos.get("todos", [])
            completed_todos = [todo for todo in raw_todos if todo.get("completed")]
            filtered_todos_without_user_id = [
                {
                    "id": todo.get("id"),
                    "todo": todo.get("todo"),
                    "complete": todo.get("completed"),
                }
                for todo in raw_todos
            ]
            report = {
                "total": todos.get("total"),
                "completed": len(completed_todos),
                "items": filtered_todos_without_user_id,
            }
            return report

    async def build_report(self, user_id: int) -> Job:
        try:
            async with asyncio.TaskGroup() as tg:
                task_user: asyncio.Task = tg.create_task(
                    UserService().get_formated_user_data(user_id)
                )
                task_todos: asyncio.Task = tg.create_task(
                    self.get_formated_user_todos_data(user_id)
                )

        except* UserNotFoundException as exc_group:
            raise exc_group.exceptions[0]

        report = {
            "user": task_user.result(),
            "todos": task_todos.result(),
        }
        return report


jobs: dict[int, dict] = {}
next_job_id = 1


class JobService(BaseService):
    async def run_report_background(self, job_id: int, user_id: int) -> None:
        job = jobs[job_id]
        try:
            report = await ReportService().build_report(user_id)
            job["status"] = "done"
            job["result"] = report
        except Exception as exc:
            job["status"] = "error"
            job["error"] = str(exc)

    async def create_job(self, user_id: int) -> JobStatusResponse:
        global next_job_id

        job_id = next_job_id
        next_job_id += 1

        job = {"job_id": job_id, "status": "running"}

        jobs[job_id] = job
        asyncio.create_task(self.run_report_background(job_id, user_id))

        return job

    async def get_job(self, job_id: int) -> JobResult:
        job = jobs.get(job_id)
        if job is None:
            raise JobNotFoundException
        return job


class UserService(BaseService):
    async def get_user_data(self, user_id: int) -> dict:
        response = await httpx.AsyncClient().get(f"{settings.API_URL}/{user_id}")
        if response.status_code == 404:
            raise UserNotFoundException
        return response.json()

    async def get_formated_user_data(self, user_id: int) -> User:
        user_data = await self.get_user_data(user_id)
        user = {
            "user_id": user_data.get("id"),
            "user_name": user_data.get("firstName"),
            "email": user_data.get("email"),
        }
        return user
