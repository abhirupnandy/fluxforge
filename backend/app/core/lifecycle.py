# backend/app/core/lifecycle.py

from app.database.base import Base
from app.database.models import *
from app.database.session import engine


async def init_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)