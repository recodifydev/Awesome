from pydantic import BaseModel
from typing import Optional

class CommandRequest(BaseModel):
    command: str
    timeout: Optional[int] = 60

class CommandResponse(BaseModel):
    process_id: str
    output: str
    exit_code: Optional[int]
    error: Optional[str]