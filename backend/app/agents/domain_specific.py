from typing import AsyncGenerator, List, Optional, Dict, Any
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from ..tools.base import BaseTool
from .base import BaseAIAgent

class DataAnalysisAgent(BaseAIAgent):
    """Agent specialized for data analysis tasks."""
    
    def __init__(
        self,
        name: str,
        tools: Optional[List[BaseTool]] = None,
        description: str = "I specialize in data analysis, visualization, and insights.",
        model: str = "gemini-pro"
    ):
        super().__init__(name=name, description=description, model=model)
        self.tools = tools or []
        
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute data analysis tasks."""
        # Add data context to prompt
        data_context = ctx.session.state.get('data_context', {})
        prompt = f"""
        Data Analysis Task:
        {ctx.message.content}
        
        Available Data Context:
        {data_context}
        """
        
        response = await self.model_instance.generate_content_async(
            prompt,
            tools=[tool.to_dict() for tool in self.tools]
        )
        
        yield Event(
            author=self.name,
            content=response.text,
            actions=response.tool_calls
        )

class SecurityAgent(BaseAIAgent):
    """Agent specialized for security analysis and monitoring."""
    
    def __init__(
        self,
        name: str,
        tools: Optional[List[BaseTool]] = None,
        description: str = "I handle security analysis and monitoring.",
        model: str = "gemini-pro"
    ):
        super().__init__(name=name, description=description, model=model)
        self.tools = tools or []
        
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute security-related tasks."""
        security_context = ctx.session.state.get('security_context', {})
        prompt = f"""
        Security Task:
        {ctx.message.content}
        
        Security Context:
        {security_context}
        """
        
        response = await self.model_instance.generate_content_async(
            prompt,
            tools=[tool.to_dict() for tool in self.tools]
        )
        
        yield Event(
            author=self.name,
            content=response.text,
            actions=response.tool_calls
        )

class DevOpsAgent(BaseAIAgent):
    """Agent specialized for DevOps tasks."""
    
    def __init__(
        self,
        name: str,
        tools: Optional[List[BaseTool]] = None,
        description: str = "I handle DevOps tasks including deployment and infrastructure.",
        model: str = "gemini-pro"
    ):
        super().__init__(name=name, description=description, model=model)
        self.tools = tools or []
        
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute DevOps tasks."""
        infra_context = ctx.session.state.get('infrastructure_context', {})
        prompt = f"""
        DevOps Task:
        {ctx.message.content}
        
        Infrastructure Context:
        {infra_context}
        """
        
        response = await self.model_instance.generate_content_async(
            prompt,
            tools=[tool.to_dict() for tool in self.tools]
        )
        
        yield Event(
            author=self.name,
            content=response.text,
            actions=response.tool_calls
        )

class QAAgent(BaseAIAgent):
    """Agent specialized for quality assurance and testing."""
    
    def __init__(
        self,
        name: str,
        tools: Optional[List[BaseTool]] = None,
        description: str = "I handle testing and quality assurance tasks.",
        model: str = "gemini-pro"
    ):
        super().__init__(name=name, description=description, model=model)
        self.tools = tools or []
        
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute QA tasks."""
        test_context = ctx.session.state.get('test_context', {})
        prompt = f"""
        QA Task:
        {ctx.message.content}
        
        Test Context:
        {test_context}
        """
        
        response = await self.model_instance.generate_content_async(
            prompt,
            tools=[tool.to_dict() for tool in self.tools]
        )
        
        yield Event(
            author=self.name,
            content=response.text,
            actions=response.tool_calls
        )