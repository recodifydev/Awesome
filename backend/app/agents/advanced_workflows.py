from typing import AsyncGenerator, List, Dict, Any, Optional
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from .base import BaseAIAgent
from .workflow import TaskSequencer, TaskParallelizer, TaskLooper

class PipelineWorkflow:
    """Implements a pipeline pattern where each stage processes and transforms data."""
    
    def __init__(self, stages: List[BaseAIAgent]):
        self.pipeline = TaskSequencer(
            name="Pipeline",
            sub_agents=stages
        )
    
    async def process(self, ctx: InvocationContext):
        """Process data through the pipeline."""
        async for event in self.pipeline.run_async(ctx):
            yield event

class MapReduceWorkflow:
    """Implements a map-reduce pattern for parallel data processing."""
    
    def __init__(
        self,
        mapper: BaseAIAgent,
        reducer: BaseAIAgent,
        num_parallel: int = 3
    ):
        self.mappers = [mapper for _ in range(num_parallel)]
        self.reducer = reducer
        self.map_stage = TaskParallelizer(
            name="MapStage",
            sub_agents=self.mappers
        )
        self.workflow = TaskSequencer(
            name="MapReduce",
            sub_agents=[self.map_stage, self.reducer]
        )
    
    async def process(self, ctx: InvocationContext):
        """Execute map-reduce workflow."""
        async for event in self.workflow.run_async(ctx):
            yield event

class RetryCatchWorkflow:
    """Implements a retry pattern with error handling."""
    
    def __init__(
        self,
        main_agent: BaseAIAgent,
        fallback_agent: BaseAIAgent,
        max_retries: int = 3
    ):
        self.main_agent = main_agent
        self.fallback_agent = fallback_agent
        self.max_retries = max_retries
        
    async def process(self, ctx: InvocationContext):
        """Execute with retry logic."""
        retries = 0
        while retries < self.max_retries:
            try:
                async for event in self.main_agent.run_async(ctx):
                    if event.error:
                        retries += 1
                        continue
                    yield event
                break  # Success, exit loop
            except Exception:
                retries += 1
        
        if retries == self.max_retries:
            # Use fallback agent
            async for event in self.fallback_agent.run_async(ctx):
                yield event

class CircuitBreakerWorkflow:
    """Implements circuit breaker pattern for fault tolerance."""
    
    def __init__(
        self,
        primary_agent: BaseAIAgent,
        fallback_agent: BaseAIAgent,
        error_threshold: int = 5,
        reset_timeout: int = 60
    ):
        self.primary_agent = primary_agent
        self.fallback_agent = fallback_agent
        self.error_threshold = error_threshold
        self.reset_timeout = reset_timeout
        self.error_count = 0
        self.is_open = False
        
    async def process(self, ctx: InvocationContext):
        """Execute with circuit breaker logic."""
        if self.is_open:
            # Circuit is open, use fallback
            async for event in self.fallback_agent.run_async(ctx):
                yield event
            return
            
        try:
            async for event in self.primary_agent.run_async(ctx):
                if event.error:
                    self.error_count += 1
                    if self.error_count >= self.error_threshold:
                        self.is_open = True
                    yield Event(
                        author=self.primary_agent.name,
                        content="Error occurred, incrementing error count.",
                        actions=EventActions(error=True)
                    )
                else:
                    self.error_count = 0  # Reset on success
                    yield event
        except Exception as e:
            self.error_count += 1
            if self.error_count >= self.error_threshold:
                self.is_open = True
            async for event in self.fallback_agent.run_async(ctx):
                yield event

class SagaWorkflow:
    """Implements saga pattern for distributed transactions."""
    
    def __init__(self, steps: List[Dict[str, BaseAIAgent]]):
        """
        Initialize with steps containing forward and compensating actions.
        steps = [
            {
                'forward': agent1,
                'compensate': compensating_agent1
            },
            ...
        ]
        """
        self.steps = steps
        
    async def process(self, ctx: InvocationContext):
        """Execute saga with compensation on failure."""
        completed_steps = []
        
        # Forward pass
        for step in self.steps:
            try:
                async for event in step['forward'].run_async(ctx):
                    if event.error:
                        raise Exception("Step failed")
                    yield event
                completed_steps.append(step)
            except Exception:
                # Compensation (rollback)
                for completed in reversed(completed_steps):
                    async for event in completed['compensate'].run_async(ctx):
                        yield event
                return
                
        yield Event(
            author="SagaWorkflow",
            content="All steps completed successfully"
        )