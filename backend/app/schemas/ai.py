from pydantic import BaseModel
from typing import List, Optional

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7
    stop: Optional[List[str]] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7

class CompletionResponse(BaseModel):
    choices: List[dict]

class ChatResponse(BaseModel):
    choices: List[dict]