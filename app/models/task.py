import enum
import uuid

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import base


class TaskStatus(str, enum.Enum):
    created = "created"
    in_progress = "in_progress"
    done = "done"


class Task(base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.created, nullable=False)
