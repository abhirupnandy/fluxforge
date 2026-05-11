from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.ws import router as ws_router
from app.core.config import settings
from app.core.lifecycle import init_database
from app.database.session import AsyncSessionLocal
from app.queue.manager import QueueManager
from app.websocket.broadcaster import Broadcaster
from app.websocket.manager import WebsocketManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    ws_manager=WebsocketManager(); broadcaster=Broadcaster(ws_manager)
    queue=QueueManager(AsyncSessionLocal,broadcaster,settings.max_concurrent_downloads,settings.max_concurrent_encodes)
    await queue.start()
    app.state.websocket_manager=ws_manager
    app.state.broadcaster=broadcaster
    app.state.queue_manager=queue
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(ws_router)
