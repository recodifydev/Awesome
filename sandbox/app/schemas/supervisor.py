from pydantic import BaseModel
from typing import List
from datetime import datetime

class ServiceStatus(BaseModel):
    name: str
    status: str
    uptime: Optional[datetime]
    memory_usage: Optional[float]
    cpu_usage: Optional[float]

class ServiceOperation(BaseModel):
    name: str
    operation: str  # start, stop, restart
    timeout: Optional[int] = 30