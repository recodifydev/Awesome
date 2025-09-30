from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..services.agents import get_agent_service
from ..schemas.agent import AgentRequest, AgentResponse
from ..evaluation.evaluator import AgentEvaluation

router = APIRouter()

@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Run an agent with the given input."""
    agent_service = get_agent_service()
    try:
        response = await agent_service.run_agent(
            agent_type=request.agent_type,
            input_text=request.input,
            context=request.context
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate", response_model=Dict[str, Any])
async def evaluate_agent(agent_module: str, eval_set_path: str):
    """Evaluate an agent using the specified eval set."""
    evaluator = AgentEvaluation(agent_module=agent_module)
    try:
        results = await evaluator.evaluate_eval_set(eval_set_path)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))