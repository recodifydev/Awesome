from fastapi import APIRouter, HTTPException, Depends
from app.services.shell_service import ShellService
from app.schemas.shell import CommandRequest, CommandResponse
from typing import Optional

router = APIRouter()
shell_service = ShellService()

@router.post("/execute", response_model=CommandResponse)
async def execute_command(command: CommandRequest):
    """Execute a shell command in the sandbox environment."""
    result = await shell_service.execute_command(command.command)
    return result

@router.get("/{process_id}/status")
async def get_process_status(process_id: str):
    """Get the status of a running process."""
    return await shell_service.get_process_status(process_id)

@router.post("/{process_id}/input")
async def send_process_input(process_id: str, input_data: str):
    """Send input to a running process."""
    return await shell_service.send_process_input(process_id, input_data)

@router.delete("/{process_id}")
async def kill_process(process_id: str):
    """Kill a running process."""
    return await shell_service.kill_process(process_id)