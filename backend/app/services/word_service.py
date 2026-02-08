from sqlalchemy.orm import Session
from app.models.word import Word
from app.services.llm_service import generate_word_data
from typing import Optional
import uuid


async def create_word_with_llm(db: Session, word_text: str, source: str = "manual") -> Word:
    """
    Create a word and generate LLM data if not already exists.
    """
    # Check if word already exists
    existing_word = db.query(Word).filter(Word.word == word_text.lower()).first()
    if existing_word:
        return existing_word
    
    # Generate LLM data
    llm_data = await generate_word_data(word_text)
    
    # Create word
    new_word = Word(
        word=word_text.lower(),
        meaning=llm_data["meaning"],
        example_sentence_1=llm_data["example_sentence_1"],
        example_sentence_2=llm_data["example_sentence_2"],
        source=source,
    )
    
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    
    return new_word


def get_word_by_id(db: Session, word_id: uuid.UUID) -> Optional[Word]:
    """Get a word by ID."""
    return db.query(Word).filter(Word.id == word_id).first()


def get_all_words(db: Session, skip: int = 0, limit: int = 100):
    """Get all words with pagination."""
    return db.query(Word).offset(skip).limit(limit).all()
