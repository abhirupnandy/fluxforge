from datetime import UTC, datetime
from app.schemas.websocket import WebSocketEvent
from app.websocket.manager import WebsocketManager
class Broadcaster:
    def __init__(self,ws_manager:WebsocketManager): self.ws_manager=ws_manager
    async def emit(self,event:str,task_id:str,data:dict)->None:
        await self.ws_manager.broadcast(WebSocketEvent(event=event,task_id=task_id,timestamp=datetime.now(UTC),data=data).model_dump(mode='json'))
