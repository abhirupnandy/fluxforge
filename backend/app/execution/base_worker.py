import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.execution.subprocess_runner import SubprocessRunner
from app.repositories.task_repository import TaskRepository
from app.websocket.broadcaster import Broadcaster
class BaseWorker:
    def __init__(self, db: AsyncSession, broadcaster: Broadcaster):
        self.repo=TaskRepository(db); self.runner=SubprocessRunner(); self.broadcaster=broadcaster; self.cancel_event=asyncio.Event()
    def cancel(self)->None: self.cancel_event.set()
