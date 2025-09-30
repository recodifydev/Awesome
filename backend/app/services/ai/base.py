from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

class AIService(ABC):
    """Base class for AI service implementations."""
    
    @abstractmethod
    async def generate_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate code completion."""
        pass
    
    @abstractmethod
    async def generate_chat_response(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Generate chat response."""
        pass