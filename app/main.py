from fastapi import FastAPI

from app.api import tasks

app = FastAPI(title="Task Manager")

app.include_router(tasks.router)
