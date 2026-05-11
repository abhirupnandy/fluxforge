from datetime import datetime
from typing import Any
from pydantic import BaseModel
class WebSocketEvent(BaseModel): event:str; task_id:str; timestamp:datetime; data:dict[str,Any]
