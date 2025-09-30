import psutil
import docker
from typing import List, Dict
import asyncio

class SupervisorService:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.services: Dict[str, dict] = {}

    async def get_all_status(self) -> List[dict]:
        """Get status of all managed services."""
        statuses = []
        for name, service in self.services.items():
            status = await self._get_service_status(name)
            statuses.append(status)
        return statuses

    async def start_service(self, service_name: str):
        """Start a service."""
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} not found")
            
        service = self.services[service_name]
        if service.get("container"):
            await self._start_container(service["container"])
        elif service.get("process"):
            await self._start_process(service["process"])

    async def stop_service(self, service_name: str):
        """Stop a service."""
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} not found")
            
        service = self.services[service_name]
        if service.get("container"):
            await self._stop_container(service["container"])
        elif service.get("process"):
            await self._stop_process(service["process"])

    async def restart_service(self, service_name: str):
        """Restart a service."""
        await self.stop_service(service_name)
        await self.start_service(service_name)

    async def _get_service_status(self, service_name: str) -> dict:
        """Get status of a specific service."""
        service = self.services.get(service_name)
        if not service:
            return {
                "name": service_name,
                "status": "not_found"
            }

        if service.get("container"):
            return await self._get_container_status(service["container"])
        elif service.get("process"):
            return await self._get_process_status(service["process"])

    async def _start_container(self, container_id: str):
        """Start a Docker container."""
        container = self.docker_client.containers.get(container_id)
        container.start()

    async def _stop_container(self, container_id: str):
        """Stop a Docker container."""
        container = self.docker_client.containers.get(container_id)
        container.stop()

    async def _start_process(self, cmd: str):
        """Start a process."""
        process = await asyncio.create_subprocess_shell(cmd)
        return process

    async def _stop_process(self, process):
        """Stop a process."""
        try:
            process.terminate()
            await process.wait()
        except ProcessLookupError:
            pass