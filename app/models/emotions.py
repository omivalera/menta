from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    mood = Column(String, nullable=False)  # Ej: "feliz", "triste", "ansioso", etc.
    note = Column(String, nullable=True)

    user = relationship("User", backref="emotions")
