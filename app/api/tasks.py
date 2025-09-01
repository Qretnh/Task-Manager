from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.services.db.tasks as db_tasks
from app.core.logger import logger
from app.db.session import get_session
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    logger.info(f"Creating task: {task}")
    return await db_tasks.create_task(session, task)


@router.get("/{task_id}", response_model=TaskOut)
async def read_task(task_id: str, session: AsyncSession = Depends(get_session)):
    db_task = await db_tasks.get_task(session, task_id)
    logger.info(f"Getting task: {task_id}")
    if not db_task:
        logger.warning(f"Task {task_id} wasn't found")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task {task_id} successfully find")
    return db_task


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    logger.info(f"Getting list for: {skip}/{limit} tasks")
    tasks = await db_tasks.get_tasks(session, skip, limit)
    logger.info(f"founded {len(tasks)} tasks")
    return tasks


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: str, task: TaskUpdate, session: AsyncSession = Depends(get_session)
):
    logger.info(f"Request for updating task: {task_id}")
    db_task = await db_tasks.update_task(session, task_id, task)
    if not db_task:
        logger.warning(f"Request cancelled: task {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task {task_id} successfully updated")
    return db_task


@router.delete("/{task_id}", response_model=TaskOut)
async def delete_task(task_id: str, session: AsyncSession = Depends(get_session)):
    logger.info(f"Request for deleting task: {task_id}")
    db_task = await db_tasks.delete_task(session, task_id)
    if not db_task:
        logger.warning(f"Request cancelled: task {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task {task_id} successfully deleted")
    return db_task
