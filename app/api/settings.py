from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.models.settings import UserSetting

router = APIRouter()

@router.get("/{user_id}")
async def get_settings(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserSetting).where(UserSetting.user_id == user_id))
    settings_list = result.scalars().all()
    
    # Transform to dict {service_type: {provider, model}}
    resp = {}
    for s in settings_list:
        resp[s.service_type] = {
            "provider": s.provider,
            "model": s.model_name
        }
    return resp

@router.post("/{user_id}")
async def update_settings(user_id: UUID, settings: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    # Delete old settings
    await db.execute(delete(UserSetting).where(UserSetting.user_id == user_id))
    
    # Add new settings
    for service_type, config in settings.items():
        new_setting = UserSetting(
            user_id=user_id,
            service_type=service_type,
            provider=config.get("provider"),
            model_name=config.get("model")
        )
        db.add(new_setting)
    
    await db.commit()
    return {"status": "success"}