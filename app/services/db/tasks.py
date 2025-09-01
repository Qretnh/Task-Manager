from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_task(db: AsyncSession, task_id) -> Task | None:
    if isinstance(task_id, str):
        task_id = UUID(task_id)
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Task]:
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()


async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    db_task = Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(db: AsyncSession, task_id, task_data: TaskUpdate) -> Task | None:
    db_task = await get_task(db, task_id)
    if not db_task:
        return None

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id) -> Task | None:
    db_task = await get_task(db, task_id)
    if not db_task:
        return None

    await db.delete(db_task)
    await db.commit()
    return db_task
