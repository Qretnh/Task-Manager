import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.session import get_session
from app.main import app
from app.models.base import base

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    DATABASE_URL, future=True, echo=False, connect_args={"check_same_thread": False}
)
SessionTest = async_sessionmaker(engine_test, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)


@pytest_asyncio.fixture()
async def session(prepare_db):
    async with SessionTest() as s:
        yield s


@pytest_asyncio.fixture()
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
