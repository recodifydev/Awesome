from fastapi import APIRouter, HTTPException
from app.services.file_service import FileService
from app.schemas.file import FileOperation, FileContent
from typing import List

router = APIRouter()
file_service = FileService()

@router.post("/read", response_model=FileContent)
async def read_file(operation: FileOperation):
    """Read content from a file in the sandbox."""
    content = await file_service.read_file(operation.path)
    return FileContent(content=content)

@router.post("/write")
async def write_file(operation: FileOperation):
    """Write content to a file in the sandbox."""
    await file_service.write_file(operation.path, operation.content)
    return {"status": "success"}

@router.post("/search")
async def search_files(pattern: str) -> List[str]:
    """Search for files matching a pattern."""
    return await file_service.search_files(pattern)

@router.post("/replace")
async def replace_in_file(operation: FileOperation):
    """Replace content in a file."""
    await file_service.replace_in_file(
        operation.path,
        operation.old_content,
        operation.new_content
    )
    return {"status": "success"}