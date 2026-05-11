from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.task import TaskModel
from app.queue.state_machine import ensure_transition
from app.schemas.task import TaskState, TaskType


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_type: TaskType, payload: dict) -> TaskModel:
        obj = TaskModel(task_type=task_type.value, payload=payload, state=TaskState.PENDING.value)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def list(self) -> list[TaskModel]:
        return (await self.db.execute(select(TaskModel).order_by(TaskModel.created_at.desc()))).scalars().all()

    async def get(self, task_id: str) -> TaskModel | None:
        return await self.db.get(TaskModel, task_id)

    async def update_state(self, task: TaskModel, new_state: TaskState) -> TaskModel:
        ensure_transition(TaskState(task.state), new_state)
        task.state = new_state.value
        if new_state in {TaskState.STARTING, TaskState.RUNNING} and not task.started_at:
            task.started_at = datetime.utcnow()
        if new_state in {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED}:
            task.completed_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def append_log(self, task: TaskModel, line: str) -> None:
        task.logs = (task.logs or "") + line + "\n"
        await self.db.commit()

    async def update_progress(self, task: TaskModel, p: float) -> None:
        task.progress = max(0.0, min(100.0, p))
        await self.db.commit()

    async def fail(self, task: TaskModel, msg: str) -> None:
        task.error_message = msg
        await self.db.commit()
