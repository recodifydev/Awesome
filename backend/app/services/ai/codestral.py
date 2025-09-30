import aiohttp
import os
from typing import Dict, Any
from .base import AIService

class CodestralService(AIService):
    """Implementation of Codestral AI service."""
    
    def __init__(self):
        self.api_key = os.getenv("CODESTRAL_API_KEY")
        self.completion_endpoint = os.getenv("CODESTRAL_COMPLETION_ENDPOINT")
        self.chat_endpoint = os.getenv("CODESTRAL_CHAT_ENDPOINT")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate code completion using Codestral API."""
        async with aiohttp.ClientSession() as session:
            payload = {
                "prompt": prompt,
                "max_tokens": kwargs.get("max_tokens", 2048),
                "temperature": kwargs.get("temperature", 0.7),
                "stop": kwargs.get("stop", ["\n\n"])
            }
            
            async with session.post(self.completion_endpoint, json=payload, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()
    
    async def generate_chat_response(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Generate chat response using Codestral API."""
        async with aiohttp.ClientSession() as session:
            payload = {
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 2048),
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            async with session.post(self.chat_endpoint, json=payload, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()