from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.emotions import Emotion
from app.services.recommendations import generate_recommendations
from app.database import SessionLocal
from app.models.users import User
from app.routes.auth import get_current_user

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[str])
async def get_recommendations(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Emotion).where(Emotion.user_id == current_user.id).order_by(Emotion.date))
    emotions = result.scalars().all()
    recs = generate_recommendations(emotions)
    return recs
