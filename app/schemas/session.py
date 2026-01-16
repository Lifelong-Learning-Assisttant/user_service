from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ChatSessionBase(BaseModel):
    session_id: str
    title: Optional[str] = None

class ChatSessionCreate(ChatSessionBase):
    user_id: UUID

class ChatSessionResponse(ChatSessionBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True