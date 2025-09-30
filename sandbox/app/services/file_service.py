import os
import glob
from typing import List
import aiofiles
import re

class FileService:
    def __init__(self):
        self.sandbox_root = os.getenv("SANDBOX_ROOT", "/sandbox")

    async def read_file(self, path: str) -> str:
        """Read content from a file in the sandbox."""
        full_path = os.path.join(self.sandbox_root, path)
        self._validate_path(full_path)
        
        async with aiofiles.open(full_path, mode='r') as file:
            content = await file.read()
        return content

    async def write_file(self, path: str, content: str):
        """Write content to a file in the sandbox."""
        full_path = os.path.join(self.sandbox_root, path)
        self._validate_path(full_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        async with aiofiles.open(full_path, mode='w') as file:
            await file.write(content)

    async def search_files(self, pattern: str) -> List[str]:
        """Search for files matching a pattern."""
        full_pattern = os.path.join(self.sandbox_root, pattern)
        matches = glob.glob(full_pattern, recursive=True)
        return [os.path.relpath(p, self.sandbox_root) for p in matches]

    async def replace_in_file(self, path: str, old_content: str, new_content: str):
        """Replace content in a file."""
        content = await self.read_file(path)
        updated_content = content.replace(old_content, new_content)
        await self.write_file(path, updated_content)

    def _validate_path(self, path: str):
        """Validate file path is within sandbox."""
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(self.sandbox_root):
            raise ValueError("Access denied: Path outside sandbox")