from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.emotions import Emotion
from app.schemas.emotions import EmotionCreate, EmotionRead
from app.models.users import User
from app.database import SessionLocal
from app.routes.auth import get_current_user

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=EmotionRead)
async def create_emotion(emotion: EmotionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_emotion = Emotion(**emotion.dict(), user_id=current_user.id)
    db.add(new_emotion)
    await db.commit()
    await db.refresh(new_emotion)
    return new_emotion

@router.get("/", response_model=list[EmotionRead])
async def get_emotions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Emotion).where(Emotion.user_id == current_user.id))
    return result.scalars().all()
