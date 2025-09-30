from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now()

class Session(BaseModel):
    id: str
    name: str
    created_at: datetime = datetime.now()
    messages: List[Message] = []
    active: bool = True
    user_id: Optional[str] = None

class User(BaseModel):
    id: str
    username: str
    hashed_password: str
    created_at: datetime = datetime.now()
    is_active: bool = True