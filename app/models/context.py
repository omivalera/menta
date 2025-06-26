from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class UserContext(Base):
    __tablename__ = "user_context"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    mood = Column(String, nullable=False)
    note = Column(String, nullable=True)

    # Contexto extendido
    location = Column(String, nullable=True)         # Ej: "Santiago, Chile"
    weather = Column(String, nullable=True)          # Ej: "Soleado"
    activity_level = Column(Float, nullable=True)    # Ej: 3.5 (escala 1-5)
    sleep_hours = Column(Float, nullable=True)       # Ej: 6.0

    user = relationship("User", back_populates="contexts")
