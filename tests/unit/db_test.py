from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.db import tasks as task_module
from app.services.db.tasks import create_task, delete_task, update_task


@pytest.mark.asyncio
async def test_create_task():
    mock_db = AsyncMock()
    payload = TaskCreate(title="Test", description="Desc")
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    task = await create_task(mock_db, payload)
    assert task.title == payload.title
    assert task.description == payload.description
    mock_db.add.assert_called_once_with(task)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(task)


@pytest.mark.asyncio
async def test_update_task_found():
    task_id = uuid4()
    existing_task = Task(
        id=task_id, title="Old", description="Old desc", status="created"
    )
    mock_db = AsyncMock()

    task_module.get_task = AsyncMock(return_value=existing_task)

    update_payload = TaskUpdate(title="New", description="in_progress")
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    updated_task = await update_task(mock_db, task_id, update_payload)
    assert updated_task.title == "New"
    assert updated_task.description == "in_progress"


@pytest.mark.asyncio
async def test_update_task_not_found():
    mock_db = AsyncMock()
    from app.services.db import tasks as task_module

    task_module.get_task = AsyncMock(return_value=None)

    update_payload = TaskUpdate(title="New")
    result = await update_task(mock_db, uuid4(), update_payload)
    assert result is None


@pytest.mark.asyncio
async def test_delete_task_not_found():
    mock_db = AsyncMock()
    from app.services.db import tasks as task_module

    task_module.get_task = AsyncMock(return_value=None)

    result = await delete_task(mock_db, uuid4())
    assert result is None
