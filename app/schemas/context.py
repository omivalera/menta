from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserContextBase(BaseModel):
    mood: str
    note: Optional[str] = None
    location: Optional[str] = None
    weather: Optional[str] = None
    activity_level: Optional[float] = None
    sleep_hours: Optional[float] = None

class UserContextCreate(UserContextBase):
    pass

class UserContext(UserContextBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
