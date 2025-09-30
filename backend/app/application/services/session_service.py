from fastapi import HTTPException
from app.domain.models.entities import Session, Message
from app.application.schemas.session import SessionCreate, MessageCreate
from app.main import db, redis_client
import json
import asyncio
from datetime import datetime
from typing import AsyncGenerator

class SessionService:
    async def create_session(self, session: SessionCreate, user_id: str) -> Session:
        session_data = Session(
            id=str(await db.sessions.count_documents({})),
            name=session.name,
            user_id=user_id
        )
        await db.sessions.insert_one(session_data.dict())
        return session_data

    async def list_sessions(self, user_id: str):
        cursor = db.sessions.find({"user_id": user_id})
        sessions = []
        async for session in cursor:
            sessions.append(Session(**session))
        return sessions

    async def add_message(self, session_id: str, message: MessageCreate, user_id: str):
        session = await db.sessions.find_one({"id": session_id, "user_id": user_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        message_data = Message(
            role=message.role,
            content=message.content
        )

        await db.sessions.update_one(
            {"id": session_id},
            {"$push": {"messages": message_data.dict()}}
        )

        # Publish message to Redis for SSE
        await redis_client.publish(
            f"session:{session_id}",
            json.dumps(message_data.dict())
        )
        return message_data

    async def stream_session(self, session_id: str, user_id: str) -> AsyncGenerator:
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"session:{session_id}")

        try:
            while True:
                message = await pubsub.get_message()
                if message and message["type"] == "message":
                    yield {
                        "event": "message",
                        "data": message["data"].decode()
                    }
                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(f"session:{session_id}")