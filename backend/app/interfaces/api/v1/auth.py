from fastapi import APIRouter, HTTPException, Depends
from app.application.services.auth_service import AuthService
from app.application.schemas.auth import UserCreate, UserLogin, Token

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    return await auth_service.register_user(user)

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    return await auth_service.login_user(user)

@router.post("/refresh", response_model=Token)
async def refresh_token(current_token: str = Depends(auth_service.get_current_token)):
    return await auth_service.refresh_token(current_token)