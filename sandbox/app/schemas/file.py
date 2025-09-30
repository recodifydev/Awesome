from pydantic import BaseModel
from typing import Optional

class FileOperation(BaseModel):
    path: str
    content: Optional[str]
    old_content: Optional[str]
    new_content: Optional[str]

class FileContent(BaseModel):
    content: str