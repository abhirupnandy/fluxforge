from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
class TaskType(str, Enum): DOWNLOAD='DOWNLOAD'; ENCODE='ENCODE'
class TaskState(str, Enum): PENDING='PENDING'; QUEUED='QUEUED'; STARTING='STARTING'; RUNNING='RUNNING'; COMPLETED='COMPLETED'; FAILED='FAILED'; CANCELLING='CANCELLING'; CANCELLED='CANCELLED'
class TaskCreate(BaseModel): payload: dict[str, Any]=Field(default_factory=dict)
class TaskRead(BaseModel):
 id:str; task_type:TaskType; state:TaskState; progress:float; payload:dict[str,Any]; logs:str|None; retry_count:int; error_message:str|None; created_at:datetime; updated_at:datetime; started_at:datetime|None; completed_at:datetime|None
 model_config={'from_attributes':True}
