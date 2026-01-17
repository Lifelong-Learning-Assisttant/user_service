from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class XPUpdateRequest(BaseModel):
    amount: int

@router.get("/{user_id}/xp")
async def get_user_xp(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"xp": user.xp}

@router.post("/{user_id}/add_xp")
async def add_user_xp(user_id: str, body: XPUpdateRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_xp = user.xp + body.amount
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(xp=new_xp)
    )
    await db.commit()
    return {"status": "success", "new_xp": new_xp}