from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.application.services.session_service import SessionService
from app.application.schemas.session import SessionCreate, SessionResponse, MessageCreate
from app.application.services.auth_service import AuthService
from sse_starlette.sse import EventSourceResponse

router = APIRouter()
session_service = SessionService()
auth_service = AuthService()

@router.post("", response_model=SessionResponse)
async def create_session(
    session: SessionCreate,
    user = Depends(auth_service.get_current_user)
):
    return await session_service.create_session(session, user.id)

@router.get("", response_model=List[SessionResponse])
async def list_sessions(user = Depends(auth_service.get_current_user)):
    return await session_service.list_sessions(user.id)

@router.get("/{session_id}/stream")
async def stream_session(
    session_id: str,
    user = Depends(auth_service.get_current_user)
):
    return EventSourceResponse(
        session_service.stream_session(session_id, user.id)
    )

@router.post("/{session_id}/messages")
async def add_message(
    session_id: str,
    message: MessageCreate,
    user = Depends(auth_service.get_current_user)
):
    return await session_service.add_message(session_id, message, user.id)