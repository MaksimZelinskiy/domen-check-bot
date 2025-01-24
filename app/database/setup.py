from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import Date, cast, func, insert, select, update

from data.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.schema import CreateTable

from .repo.requests import RequestsRepo
from database.models.users import User
from database.models.roles import Role
from database.models.base import Base

from data.config import STANDARD_ROLES  

POSTGRES_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def create_engine(postgres_url: str = POSTGRES_URL, echo: bool = False):
    engine = create_async_engine(
        postgres_url,
        poolclass=AsyncAdaptedQueuePool,
        pool_size=20,
        max_overflow=80,
        pool_timeout=30,
        pool_pre_ping=True,
        pool_recycle=1800,
        query_cache_size=1200,
        future=True,
        echo=echo,
    )
    return engine

def create_session_pool(engine) -> async_sessionmaker[AsyncSession]:
    session_pool = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return session_pool

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Контекстный менеджер для получения сессии базы данных."""
    engine = create_engine()
    session_pool = create_session_pool(engine)
    
    try:
        async with session_pool() as session:
            yield session
    finally:
        await engine.dispose()

async def get_db() -> RequestsRepo:
    """Получение репозитория с активной сессией."""
    async with get_session() as session:
        return RequestsRepo(session)

async def create_tables(engine) -> None:
    """Создает таблицы в базе данных, если они не существуют."""
    async with engine.begin() as conn:
        # Сначала создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
        
    # После создания таблиц добавляем базовые роли
    session_pool = create_session_pool(engine)
    async with session_pool() as session:
        try:
            for role in STANDARD_ROLES:
                # Проверяем существование роли
                stmt = select(Role).where(Role.id == role["id"])
                existing_role = await session.execute(stmt)
                existing_role = existing_role.scalar_one_or_none()
                
                if not existing_role:
                    new_role = Role(id=role["id"], name=role["name"])
                    session.add(new_role)
            
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise