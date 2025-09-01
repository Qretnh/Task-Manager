import uuid
from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None


class TaskOut(TaskBase):
    id: uuid.UUID
    status: TaskStatus

    class Config:
        orm_mode = True
