from pydantic import BaseModel
from datetime import date

class EmotionBase(BaseModel):
    date: date
    mood: str
    note: str | None = None

class EmotionCreate(EmotionBase):
    pass

class EmotionRead(EmotionBase):
    id: int

    class Config:
        orm_mode = True
