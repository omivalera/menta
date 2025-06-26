from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.schemas.context import UserContext, UserContextCreate
from app.models.context import UserContext as UserContextModel
from app.models.users import User
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=UserContext)
async def create_context(
    context_in: UserContextCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    context = UserContextModel(
        user_id=current_user.id,
        mood=context_in.mood,
        note=context_in.note,
        location=context_in.location,
        weather=context_in.weather,
        activity_level=context_in.activity_level,
        sleep_hours=context_in.sleep_hours
    )
    db.add(context)
    await db.commit()
    await db.refresh(context)
    return context

@router.get("/", response_model=List[UserContext])
async def read_contexts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(
        UserContextModel.__table__.select().where(UserContextModel.user_id == current_user.id)
    )
    contexts = result.scalars().all()
    return contexts
