# core_db — Reusable DB Setup (Postgres + SQLite)

Drop this into any FastAPI project. Set DATABASE_URL. Write models. Done.

---

## Setup (one time per project)

### 1. Copy files
```
your_project/
├── core_db/          ← copy this folder
├── alembic/
│   ├── env.py        ← copy from alembic_template/env.py
│   └── versions/     ← empty folder
├── alembic.ini       ← copy from alembic_template/alembic.ini
├── .env
└── main.py
```

### 2. Install dependencies
```bash
pip install sqlalchemy asyncpg aiosqlite alembic python-dotenv
```

### 3. Set .env
```env
# SQLite (zero config, great for dev)
DATABASE_URL=sqlite:///./app.db

# OR Postgres
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

APP_ENV=development
```

---

## Every new app — only 3 steps

### Step 1 — Write your model
```python
# models/user.py
from sqlalchemy import Column, Integer, String
from core_db import Base

class User(Base):
    __tablename__ = "users"
    id    = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False)
    email = Column(String, unique=True)
```

### Step 2 — Wire lifespan in main.py
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
```

### Step 3 — Use in routes
```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core_db import get_db

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    ...
```

**That's it. No other config needed.**

---

## When you change a model (add column, rename, etc.)

```bash
# register your model in alembic/env.py first:
# from app.models.user import User

alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

---

## DB URL formats (auto-fixed, you don't need async driver prefix)

| You write in .env | Works? |
|---|---|
| `sqlite:///./app.db` | ✅ auto-fixed |
| `postgresql://user:pass@host/db` | ✅ auto-fixed |
| `postgresql+asyncpg://user:pass@host/db` | ✅ already correct |
| `postgres://user:pass@host/db` | ✅ auto-fixed (Heroku style) |

---

## APP_ENV behaviour

| APP_ENV | What init_db() does |
|---|---|
| `development` | connect check + auto create tables |
| `production` | connect check only → you run `alembic upgrade head` |
