import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")
def get_db_url() -> str:
    url = os.getenv("DATABASE_URL")

    if not url:
        # fallback if .env missing
        url = "sqlite+aiosqlite:///./app.db"

    # Auto-fix postgres → async
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)

    # Auto-fix sqlite → async
    if url.startswith("sqlite:///"):
        url = url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)

    return url

def is_sqlite(url: str = None) -> bool:
    return (url or get_db_url()).startswith("sqlite")


_url = get_db_url()

# SQLite doesn't support pool settings
if is_sqlite(_url):
    engine = create_async_engine(
        _url,
        echo=False,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_async_engine(
        _url,
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )
