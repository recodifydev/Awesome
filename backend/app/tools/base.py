from typing import Dict, Any, List
from pydantic import BaseModel

class ToolInput(BaseModel):
    """Base model for tool inputs."""
    name: str
    description: str
    parameters: Dict[str, Any]

class BaseTool:
    """Base class for all tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    def to_dict(self) -> dict:
        """Convert tool to dictionary format for Gemini API."""
        return {
            "name": self.name,
            "description": self.description
        }
        
    async def execute(self, **kwargs) -> Any:
        """Execute the tool functionality."""
        raise NotImplementedError("Tool must implement execute method")