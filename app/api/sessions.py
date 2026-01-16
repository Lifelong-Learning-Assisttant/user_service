from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.models.session import ChatSession
from app.schemas.session import ChatSessionCreate, ChatSessionResponse

router = APIRouter()

@router.post("/", response_model=ChatSessionResponse)
async def create_session(session_data: ChatSessionCreate, db: AsyncSession = Depends(get_db)):
    """Регистрация новой сессии для пользователя"""
    # 1. Проверяем, не существует ли уже такая сессия
    result = await db.execute(select(ChatSession).where(ChatSession.session_id == session_data.session_id))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID already exists"
        )
    
    # 2. Проверяем лимит сессий пользователя
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == session_data.user_id)
        .order_by(ChatSession.created_at.asc())
    )
    user_sessions = result.scalars().all()
    
    if len(user_sessions) >= settings.max_user_sessions:
        # Удаляем самую старую сессию
        oldest_session = user_sessions[0]
        await db.delete(oldest_session)
        # Мы не коммитим здесь, чтобы все прошло в одной транзакции
    
    # 3. Создаем новую сессию
    new_session = ChatSession(
        user_id=session_data.user_id,
        session_id=session_data.session_id,
        title=session_data.title
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

@router.get("/user/{user_id}", response_model=List[ChatSessionResponse])
async def get_user_sessions(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Получение всех сессий конкретного пользователя"""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
    )
    return result.scalars().all()

@router.delete("/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Удаление метаданных сессии"""
    await db.execute(delete(ChatSession).where(ChatSession.session_id == session_id))
    await db.commit()
    return {"status": "success"}