from typing import AsyncGenerator, Optional, Dict, Any
from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
import google.generativeai as genai
from google.generativeai.types import content_types

class BaseAIAgent(BaseAgent):
    """Base class for all AI agents in our system."""
    
    def __init__(self, name: str, description: str = "", model: str = "gemini-pro"):
        super().__init__(name=name, description=description)
        self.model = model
        self._setup_gemini()
    
    def _setup_gemini(self):
        """Configure Gemini model."""
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_instance = genai.GenerativeModel(self.model)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Default implementation for running the agent."""
        raise NotImplementedError("Subclasses must implement _run_async_impl")