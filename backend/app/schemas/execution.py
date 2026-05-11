from pydantic import BaseModel
class ProgressEvent(BaseModel): percentage:float|None=None; speed:str|None=None; eta:str|None=None; fps:float|None=None; bitrate:str|None=None; downloaded_bytes:int|None=None; total_bytes:int|None=None
class ExecutionResult(BaseModel): returncode:int; logs:list[str]
