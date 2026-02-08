from sqlalchemy import Column, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.database import Base


class UserNotes(Base):
    __tablename__ = "user_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    word_id = Column(UUID(as_uuid=True), ForeignKey("words.id"), nullable=False)
    custom_meaning = Column(Text, nullable=True)
    custom_sentence_1 = Column(Text, nullable=True)
    custom_sentence_2 = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notes")
    word = relationship("Word", back_populates="notes")

    __table_args__ = (UniqueConstraint("user_id", "word_id", name="unique_user_word_notes"),)
