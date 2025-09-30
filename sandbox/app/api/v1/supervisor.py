from fastapi import APIRouter
from app.services.supervisor_service import SupervisorService
from app.schemas.supervisor import ServiceStatus, ServiceOperation
from typing import List

router = APIRouter()
supervisor = SupervisorService()

@router.get("/status", response_model=List[ServiceStatus])
async def get_status():
    """Get status of all managed services."""
    return await supervisor.get_all_status()

@router.post("/{service_name}/start")
async def start_service(service_name: str):
    """Start a service."""
    await supervisor.start_service(service_name)
    return {"status": "started"}

@router.post("/{service_name}/stop")
async def stop_service(service_name: str):
    """Stop a service."""
    await supervisor.stop_service(service_name)
    return {"status": "stopped"}

@router.post("/{service_name}/restart")
async def restart_service(service_name: str):
    """Restart a service."""
    await supervisor.restart_service(service_name)
    return {"status": "restarted"}