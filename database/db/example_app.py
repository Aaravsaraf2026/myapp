# ─── Example: How to use core_db in any new app ──────────────────────────────
#
# 1. Copy core_db/ into your project
# 2. Set DATABASE_URL in .env
# 3. Write your models (import Base from core_db)
# 4. Done — use in FastAPI routes with Depends(get_db)
# ─────────────────────────────────────────────────────────────────────────────

# ── .env ─────────────────────────────────────────────────────────────────────
# SQLite (dev, zero config):
#   DATABASE_URL=sqlite:///./app.db
#
# Postgres (dev or prod):
#   DATABASE_URL=postgresql://user:password@localhost:5432/mydb
#
# APP_ENV=development   ← auto creates tables
# APP_ENV=production    ← skips create_all, use alembic upgrade head
# ─────────────────────────────────────────────────────────────────────────────


# ── models/user.py ───────────────────────────────────────────────────────────
from sqlalchemy import Column, Integer, String
from core_db import Base                          # ← only this import needed

class User(Base):
    __tablename__ = "users"
    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# ── main.py ──────────────────────────────────────────────────────────────────
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core_db import init_db, get_db             # ← only these two needed
from models.user import User                     # your model

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()                              # checks connection + creates tables (dev)
    yield

app = FastAPI(lifespan=lifespan)


# ── route example ────────────────────────────────────────────────────────────
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()


@app.post("/users")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
