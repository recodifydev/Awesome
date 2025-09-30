from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Agent API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connections
mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = mongodb_client.ai_agent

# Redis connection
redis_client = Redis.from_url(os.getenv("REDIS_URL"))

@app.on_event("shutdown")
async def shutdown_event():
    mongodb_client.close()
    await redis_client.close()

# Import and include routers
from app.interfaces.api.v1.session import router as session_router
from app.interfaces.api.v1.auth import router as auth_router
from app.interfaces.api.v1.shell import router as shell_router
from app.interfaces.api.v1.file import router as file_router
from app.interfaces.api.v1.supervisor import router as supervisor_router

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(session_router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(shell_router, prefix="/api/v1/shell", tags=["shell"])
app.include_router(file_router, prefix="/api/v1/file", tags=["file"])
app.include_router(supervisor_router, prefix="/api/v1/supervisor", tags=["supervisor"])