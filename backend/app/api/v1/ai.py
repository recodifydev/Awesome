from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from ..services.ai import CodestralService, HuggingFaceService
from ..schemas.ai import CompletionRequest, ChatRequest, CompletionResponse, ChatResponse

router = APIRouter()

async def get_ai_service(service_type: str = "codestral"):
    """Dependency to get the appropriate AI service."""
    if service_type.lower() == "codestral":
        return CodestralService()
    elif service_type.lower() == "huggingface":
        return HuggingFaceService()
    else:
        raise HTTPException(status_code=400, detail="Invalid service type")

@router.post("/completion", response_model=CompletionResponse)
async def generate_completion(
    request: CompletionRequest,
    service_type: str = "codestral",
    service: Any = Depends(get_ai_service)
):
    """Generate code completion."""
    try:
        response = await service.generate_completion(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stop=request.stop
        )
        return CompletionResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def generate_chat_response(
    request: ChatRequest,
    service_type: str = "codestral",
    service: Any = Depends(get_ai_service)
):
    """Generate chat response."""
    try:
        response = await service.generate_chat_response(
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))