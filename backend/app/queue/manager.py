import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.execution.registry import WORKERS
from app.queue import task_events
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskState, TaskType
from app.websocket.broadcaster import Broadcaster

class QueueManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], broadcaster: Broadcaster, max_downloads: int, max_encodes: int):
        self.session_factory=session_factory; self.broadcaster=broadcaster
        self.download_q: asyncio.Queue[str]=asyncio.Queue(); self.encode_q: asyncio.Queue[str]=asyncio.Queue()
        self.download_sem=asyncio.Semaphore(max_downloads); self.encode_sem=asyncio.Semaphore(max_encodes); self.active={}; self._dispatcher=None
    async def start(self)->None:
        if not self._dispatcher: self._dispatcher=asyncio.create_task(self._dispatch_loop())
    async def enqueue(self, task_id:str, task_type:TaskType)->None:
        await (self.download_q if task_type==TaskType.DOWNLOAD else self.encode_q).put(task_id)
    async def cancel(self, task_id:str)->None:
        w=self.active.get(task_id)
        if w: w.cancel()
    async def _dispatch_loop(self)->None:
        while True:
            if not self.download_q.empty(): asyncio.create_task(self._run_one(self.download_q,self.download_sem))
            if not self.encode_q.empty(): asyncio.create_task(self._run_one(self.encode_q,self.encode_sem))
            await asyncio.sleep(0.1)
    async def _run_one(self,q,sem)->None:
        async with sem:
            task_id=await q.get()
            async with self.session_factory() as db:
                repo=TaskRepository(db); task=await repo.get(task_id)
                if not task: return
                await repo.update_state(task,TaskState.STARTING); await repo.update_state(task,TaskState.RUNNING)
                await self.broadcaster.emit(task_events.TASK_STARTED,task.id,{})
                worker=WORKERS[task.task_type](db,self.broadcaster); self.active[task.id]=worker
                res=await worker.execute(task); self.active.pop(task.id,None)
                if worker.cancel_event.is_set(): await repo.update_state(task,TaskState.CANCELLING); await repo.update_state(task,TaskState.CANCELLED); await self.broadcaster.emit(task_events.TASK_CANCELLED,task.id,{})
                elif res.returncode==0: await repo.update_state(task,TaskState.COMPLETED); await repo.update_progress(task,100.0); await self.broadcaster.emit(task_events.TASK_COMPLETED,task.id,{})
                else: await repo.fail(task,f'Process exited with {res.returncode}'); await repo.update_state(task,TaskState.FAILED); await self.broadcaster.emit(task_events.TASK_FAILED,task.id,{})
