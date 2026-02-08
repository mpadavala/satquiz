from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_favorite import UserFavorite
from app.models.word import Word
from app.api.auth import get_current_user
from app.models.user import User
import uuid

router = APIRouter()


@router.post("/favorite/{word_id}")
async def toggle_favorite(
    word_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle favorite status for a word."""
    try:
        word_uuid = uuid.UUID(word_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid word ID")
    
    # Check if word exists
    word = db.query(Word).filter(Word.id == word_uuid).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Check if already favorited
    existing = (
        db.query(UserFavorite)
        .filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.word_id == word_uuid,
        )
        .first()
    )
    
    if existing:
        # Remove favorite
        db.delete(existing)
        db.commit()
        return {"message": "Removed from favorites", "is_favorite": False}
    else:
        # Add favorite
        favorite = UserFavorite(user_id=current_user.id, word_id=word_uuid)
        db.add(favorite)
        db.commit()
        return {"message": "Added to favorites", "is_favorite": True}


@router.get("/favorites")
async def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all favorite words for current user."""
    favorites = (
        db.query(UserFavorite)
        .filter(UserFavorite.user_id == current_user.id)
        .all()
    )
    
    words = []
    for fav in favorites:
        word = db.query(Word).filter(Word.id == fav.word_id).first()
        if word:
            words.append({
                "id": str(word.id),
                "word": word.word,
                "meaning": word.meaning,
                "example_sentence_1": word.example_sentence_1,
                "example_sentence_2": word.example_sentence_2,
                "source": word.source,
            })
    
    return words
