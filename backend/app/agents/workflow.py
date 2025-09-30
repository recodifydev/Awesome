from typing import AsyncGenerator
from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from .base import BaseAIAgent

class TaskSequencer(SequentialAgent):
    """Executes a sequence of tasks in order."""
    
    def __init__(self, name: str, sub_agents: list):
        super().__init__(name=name, sub_agents=sub_agents)

class TaskParallelizer(ParallelAgent):
    """Executes tasks in parallel."""
    
    def __init__(self, name: str, sub_agents: list):
        super().__init__(name=name, sub_agents=sub_agents)

class TaskLooper(LoopAgent):
    """Executes tasks in a loop until a condition is met."""
    
    def __init__(self, name: str, sub_agents: list, max_iterations: int = 10):
        super().__init__(name=name, sub_agents=sub_agents, max_iterations=max_iterations)

class WorkflowOrchestrator(BaseAIAgent):
    """Orchestrates complex workflows using multiple agents."""
    
    def __init__(self, name: str, workflows: dict):
        super().__init__(name=name)
        self.workflows = workflows
        
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute the appropriate workflow based on context."""
        workflow_name = await self._determine_workflow(ctx)
        workflow = self.workflows.get(workflow_name)
        
        if workflow:
            async for event in workflow.run_async(ctx):
                yield event
        else:
            yield Event(
                author=self.name,
                content=f"No workflow found for: {workflow_name}"
            )
            
    async def _determine_workflow(self, ctx: InvocationContext) -> str:
        """Determine which workflow to execute based on context."""
        response = await self.model_instance.generate_content_async(
            f"Based on this request, which workflow should I use? Options: {list(self.workflows.keys())}\n\nRequest: {ctx.message.content}"
        )
        return response.text.strip()