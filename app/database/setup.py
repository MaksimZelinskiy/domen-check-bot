from fast_api.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .repo.requests import RequestsRepo

POSTGRES_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# db: DbConfig,
def create_engine(postgres_url: str = POSTGRES_URL, echo=False):
    engine = create_async_engine(
        postgres_url,
        query_cache_size=1200,
        pool_size=50,
        max_overflow=200,
        future=True,
        echo=echo,
    )
    return engine


def create_session_pool(engine):
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool


async def get_db():
    session_pool = create_session_pool(create_engine())
    async with session_pool() as session:
        return RequestsRepo(session)
