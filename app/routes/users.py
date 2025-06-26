from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.users import User
from app.schemas.users import UserCreate, UserRead
from app.database import SessionLocal
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependencia para obtener sesión de BD
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_pw = pwd_context.hash(user.password)
    db_user = User(email=user.email, full_name=user.full_name, hashed_password=hashed_pw)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
