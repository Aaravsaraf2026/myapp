import os
from sqlalchemy import text
from .engine import engine, is_sqlite
from .base import Base
# from fastapi.exceptions import
from sqlalchemy.exc import OperationalError 

APP_ENV = os.getenv("APP_ENV", "development")  # development | production


async def _check_connection():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    print(f"✅ DB connected → {engine.url.render_as_string(hide_password=True)}")


async def _create_tables():
    """
    Only used in development + SQLite.
    Production uses Alembic → run: alembic upgrade head
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created (dev mode)")


async def _check_migration():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(
                text("SELECT version_num FROM alembic_version")
            )
            version = result.scalar()
            print(f"✅ Alembic version: {version}")

    except OperationalError:
        print("❌ Alembic not initialized.")
        print("👉 Run: alembic upgrade head")
        raise RuntimeError("Database is not migrated")
    
async def init_db():
    await _check_connection()
    await _check_migration()