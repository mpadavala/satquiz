from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.word import Word
from app.models.user_favorite import UserFavorite
from app.api.auth import get_current_user
from app.models.user import User
from pydantic import BaseModel
import uuid

router = APIRouter()


class WordResponse(BaseModel):
    id: str
    word: str
    meaning: str | None
    example_sentence_1: str | None
    example_sentence_2: str | None
    source: str
    is_favorite: bool = False

    class Config:
        from_attributes = True


@router.get("/words", response_model=List[WordResponse])
async def get_words(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all words with favorite status for current user."""
    words = db.query(Word).offset(skip).limit(limit).all()
    
    # Get user's favorite word IDs
    favorite_ids = {
        fav.word_id
        for fav in db.query(UserFavorite)
        .filter(UserFavorite.user_id == current_user.id)
        .all()
    }
    
    result = []
    for word in words:
        result.append(
            WordResponse(
                id=str(word.id),
                word=word.word,
                meaning=word.meaning,
                example_sentence_1=word.example_sentence_1,
                example_sentence_2=word.example_sentence_2,
                source=word.source,
                is_favorite=word.id in favorite_ids,
            )
        )
    
    return result


@router.get("/words/{word_id}", response_model=WordResponse)
async def get_word(
    word_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific word by ID."""
    try:
        word_uuid = uuid.UUID(word_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid word ID")
    
    word = db.query(Word).filter(Word.id == word_uuid).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Check if favorite
    is_favorite = (
        db.query(UserFavorite)
        .filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.word_id == word_uuid,
        )
        .first()
        is not None
    )
    
    return WordResponse(
        id=str(word.id),
        word=word.word,
        meaning=word.meaning,
        example_sentence_1=word.example_sentence_1,
        example_sentence_2=word.example_sentence_2,
        source=word.source,
        is_favorite=is_favorite,
    )
