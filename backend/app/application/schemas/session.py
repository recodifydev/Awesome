from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MessageCreate(BaseModel):
    content: str
    role: str = "user"

class MessageResponse(MessageCreate):
    timestamp: datetime

class SessionCreate(BaseModel):
    name: str

class SessionResponse(SessionCreate):
    id: str
    created_at: datetime
    messages: List[MessageResponse]
    active: bool
    user_id: str