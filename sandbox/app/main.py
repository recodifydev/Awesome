from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Agent Sandbox")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api.v1.shell import router as shell_router
from app.api.v1.file import router as file_router
from app.api.v1.supervisor import router as supervisor_router

# Include routers
app.include_router(shell_router, prefix="/api/v1/shell", tags=["shell"])
app.include_router(file_router, prefix="/api/v1/file", tags=["file"])
app.include_router(supervisor_router, prefix="/api/v1/supervisor", tags=["supervisor"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True
    )