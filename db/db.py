import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# --- Database --- #
load_dotenv()
DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_PORT', 5432),
    os.getenv('DB_NAME')
)
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with SessionLocal() as session:
        yield session
