from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskType
from app.services.task_service import TaskService

router = APIRouter(prefix='/tasks', tags=['Tasks'])


def service(request: Request, db: AsyncSession) -> TaskService:
    return TaskService(db, request.app.state.queue_manager, request.app.state.broadcaster)

@router.post('/download', response_model=TaskRead)
async def create_download(data: TaskCreate, request: Request, db: AsyncSession = Depends(get_db)):
    return await service(request, db).create_and_enqueue(TaskType.DOWNLOAD, data)

@router.post('/encode', response_model=TaskRead)
async def create_encode(data: TaskCreate, request: Request, db: AsyncSession = Depends(get_db)):
    return await service(request, db).create_and_enqueue(TaskType.ENCODE, data)

@router.get('', response_model=list[TaskRead])
async def list_tasks(request: Request, db: AsyncSession = Depends(get_db)):
    return await service(request, db).list_tasks()

@router.get('/{task_id}', response_model=TaskRead)
async def get_task(task_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    t = await service(request, db).get_task(task_id)
    if not t: raise HTTPException(404, 'Task not found')
    return t

@router.post('/{task_id}/cancel', response_model=TaskRead)
async def cancel(task_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    t = await service(request, db).cancel(task_id)
    if not t: raise HTTPException(404, 'Task not found')
    return t
