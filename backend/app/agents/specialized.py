from typing import AsyncGenerator, List, Optional
from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from ..tools.base import BaseTool
from .base import BaseAIAgent

class CodingAgent(BaseAIAgent):
    """Agent specialized for code-related tasks."""
    
    def __init__(
        self,
        name: str,
        tools: Optional[List[BaseTool]] = None,
        description: str = "I am a coding assistant that helps with programming tasks.",
        model: str = "gemini-pro"
    ):
        super().__init__(name=name, description=description, model=model)
        self.tools = tools or []
        
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute coding-related tasks."""
        response = await self.model_instance.generate_content_async(
            ctx.message.content,
            tools=[tool.to_dict() for tool in self.tools]
        )
        
        yield Event(
            author=self.name,
            content=response.text,
            actions=response.tool_calls
        )

class AutomationAgent(BaseAIAgent):
    """Agent specialized for automation tasks."""
    
    def __init__(
        self,
        name: str,
        tools: Optional[List[BaseTool]] = None,
        description: str = "I help automate computer interactions and workflows.",
        model: str = "gemini-pro"
    ):
        super().__init__(name=name, description=description, model=model)
        self.tools = tools or []
        
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute automation tasks."""
        response = await self.model_instance.generate_content_async(
            ctx.message.content,
            tools=[tool.to_dict() for tool in self.tools]
        )
        
        yield Event(
            author=self.name,
            content=response.text,
            actions=response.tool_calls
        )