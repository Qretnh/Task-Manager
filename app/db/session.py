from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with SessionLocal() as session:
        yield session
