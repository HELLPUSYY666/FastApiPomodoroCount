from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.settings import Settings

settings = Settings()
engine = create_async_engine(settings.db_url, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session_maker():
    return async_session_maker


async def get_db_session():
    async with async_session_maker() as session:
        yield session
