from sqlalchemy.ext.asyncio import AsyncSession

from app.queue import task_events
from app.queue.manager import QueueManager
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskRead, TaskState, TaskType
from app.websocket.broadcaster import Broadcaster


class TaskService:
    def __init__(self, db: AsyncSession, queue_manager: QueueManager, broadcaster: Broadcaster):
        self.repo = TaskRepository(db)
        self.queue = queue_manager
        self.broadcaster = broadcaster

    async def create_and_enqueue(self, task_type: TaskType, data: TaskCreate) -> TaskRead:
        task = await self.repo.create(task_type, data.payload)
        await self.broadcaster.emit(task_events.TASK_CREATED, task.id, {})
        await self.repo.update_state(task, TaskState.QUEUED)
        await self.broadcaster.emit(task_events.TASK_QUEUED, task.id, {})
        await self.queue.enqueue(task.id, task_type)
        return TaskRead.model_validate(task)

    async def list_tasks(self) -> list[TaskRead]:
        return [TaskRead.model_validate(t) for t in await self.repo.list()]

    async def get_task(self, task_id: str) -> TaskRead | None:
        t = await self.repo.get(task_id)
        return TaskRead.model_validate(t) if t else None

    async def cancel(self, task_id: str) -> TaskRead | None:
        t = await self.repo.get(task_id)
        if not t:
            return None
        await self.repo.update_state(t, TaskState.CANCELLING)
        await self.queue.cancel(task_id)
        return TaskRead.model_validate(t)
