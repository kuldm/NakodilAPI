from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field


class JobStatusResponse(BaseModel):
    job_id: int
    status: str


class User(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr


class TodoItem(BaseModel):
    id: int
    todo: str
    complete: bool


class Todo(BaseModel):
    total: int
    completed: int
    items: list[TodoItem]


class Job(BaseModel):
    user: User
    todos: Todo


class JobRunning(JobStatusResponse):
    status: Literal["running"]


class JobDone(JobStatusResponse):
    status: Literal["done"]
    result: Job


class JobFailed(JobStatusResponse):
    status: Literal["error"]
    error: str


JobResult = Annotated[JobDone | JobRunning | JobFailed, Field(discriminator="status")]


class Ping(BaseModel):
    status: str = "OK"
