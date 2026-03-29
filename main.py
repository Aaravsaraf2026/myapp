from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import os
from database.db.core import init_db, get_db
from database.models import User, Products
from repo.queue.worker import connection_manager, shutdown_manager

from contextlib import asynccontextmanager
from repo.queue.worker import (
    connection_manager,
    shutdown_manager,
    health_checker,
    message_reclaimer,
    cleanup_thread,
)

import sys
import logging
from core.logging import setup_logging
import logging

setup_logging()
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting app...")

    shutdown_manager.embedded = True

    await init_db()

    try:
        app.state.redis = connection_manager.get_client()
    except RuntimeError as e:
        
        logger.error("no redis founded") # silence uvicorn traceback
        os._exit(1)  # hard exit — bypasses Starlette's exception handling entirely

    health_checker.start()
    message_reclaimer.start()
    cleanup_thread.start()

    yield

    logger.info("App closed successfully")
    shutdown_manager.shutdown()

app = FastAPI(lifespan=lifespan)




@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Hello"}


@app.post("/seed")
async def seed_products(db: AsyncSession = Depends(get_db)):
    products = [
        Products(Product_name="iPhone", product_id=104, price=80000),
        Products(Product_name="Laptop", product_id=105, price=60000),
        Products(Product_name="Headphones", product_id=106, price=2000),
    ]

    db.add_all(products)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Duplicate product_id")


# ── route example ────────────────────────────────────────────────────────────
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Products))
    return result.scalars().all()


