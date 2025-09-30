import asyncio
import docker
import os
from typing import Dict, Optional
import uuid

class ShellService:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.processes: Dict[str, asyncio.subprocess.Process] = {}

    async def execute_command(self, command: str) -> dict:
        """Execute a command in the sandbox environment."""
        process_id = str(uuid.uuid4())
        
        try:
            # Create process
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.processes[process_id] = process
            
            # Wait for completion with timeout
            stdout, stderr = await process.communicate()
            
            return {
                "process_id": process_id,
                "output": stdout.decode(),
                "exit_code": process.returncode,
                "error": stderr.decode() if stderr else None
            }
            
        except Exception as e:
            return {
                "process_id": process_id,
                "output": "",
                "exit_code": -1,
                "error": str(e)
            }

    async def get_process_status(self, process_id: str) -> dict:
        """Get the status of a running process."""
        process = self.processes.get(process_id)
        if not process:
            return {"status": "not_found"}
            
        return {
            "status": "running" if process.returncode is None else "completed",
            "exit_code": process.returncode
        }

    async def send_process_input(self, process_id: str, input_data: str) -> dict:
        """Send input to a running process."""
        process = self.processes.get(process_id)
        if not process or process.stdin.is_closing():
            raise ValueError("Process not found or not accepting input")
            
        try:
            process.stdin.write(f"{input_data}\n".encode())
            await process.stdin.drain()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def kill_process(self, process_id: str) -> dict:
        """Kill a running process."""
        process = self.processes.get(process_id)
        if not process:
            return {"status": "not_found"}
            
        try:
            process.terminate()
            await process.wait()
            del self.processes[process_id]
            return {"status": "killed"}
        except Exception as e:
            return {"status": "error", "message": str(e)}