from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word = Column(String, unique=True, index=True, nullable=False)
    meaning = Column(Text, nullable=True)
    example_sentence_1 = Column(Text, nullable=True)
    example_sentence_2 = Column(Text, nullable=True)
    source = Column(String, default="manual")  # pdf or manual
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    favorites = relationship("UserFavorite", back_populates="word", cascade="all, delete-orphan")
    notes = relationship("UserNotes", back_populates="word", cascade="all, delete-orphan")
