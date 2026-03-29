from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .engine import engine

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    """
    FastAPI dependency. Use in routes:
        db: AsyncSession = Depends(get_db)
    """
    async with SessionLocal() as session:
        yield session
