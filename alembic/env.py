import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# ✅ your imports
from database.db.core.base import Base
from database.db.core.engine import get_db_url
from database.models import *  # IMPORTANT: registers models

# Alembic config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ FIX: metadata
target_metadata = Base.metadata

# ✅ FIX: use .env DB
config.set_main_option("sqlalchemy.url", get_db_url())


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_async_engine(
        get_db_url(),
        poolclass=pool.NullPool,
    )

    async def run():
        async with connectable.connect() as connection:
            await connection.run_sync(run_migrations)

    asyncio.run(run())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()