from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_notes import UserNotes
from app.models.word import Word
from app.api.auth import get_current_user
from app.models.user import User
from pydantic import BaseModel
import uuid

router = APIRouter()


class NotesUpdate(BaseModel):
    custom_meaning: str | None = None
    custom_sentence_1: str | None = None
    custom_sentence_2: str | None = None


@router.put("/notes/{word_id}")
async def update_notes(
    word_id: str,
    notes: NotesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update or create notes for a word."""
    try:
        word_uuid = uuid.UUID(word_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid word ID")
    
    # Check if word exists
    word = db.query(Word).filter(Word.id == word_uuid).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Get or create notes
    user_notes = (
        db.query(UserNotes)
        .filter(
            UserNotes.user_id == current_user.id,
            UserNotes.word_id == word_uuid,
        )
        .first()
    )
    
    if user_notes:
        # Update existing notes
        if notes.custom_meaning is not None:
            user_notes.custom_meaning = notes.custom_meaning
        if notes.custom_sentence_1 is not None:
            user_notes.custom_sentence_1 = notes.custom_sentence_1
        if notes.custom_sentence_2 is not None:
            user_notes.custom_sentence_2 = notes.custom_sentence_2
    else:
        # Create new notes
        user_notes = UserNotes(
            user_id=current_user.id,
            word_id=word_uuid,
            custom_meaning=notes.custom_meaning,
            custom_sentence_1=notes.custom_sentence_1,
            custom_sentence_2=notes.custom_sentence_2,
        )
        db.add(user_notes)
    
    db.commit()
    db.refresh(user_notes)
    
    return {
        "id": str(user_notes.id),
        "word_id": str(word_id),
        "custom_meaning": user_notes.custom_meaning,
        "custom_sentence_1": user_notes.custom_sentence_1,
        "custom_sentence_2": user_notes.custom_sentence_2,
        "updated_at": user_notes.updated_at.isoformat(),
    }


@router.get("/notes/{word_id}")
async def get_notes(
    word_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get notes for a word."""
    try:
        word_uuid = uuid.UUID(word_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid word ID")
    
    user_notes = (
        db.query(UserNotes)
        .filter(
            UserNotes.user_id == current_user.id,
            UserNotes.word_id == word_uuid,
        )
        .first()
    )
    
    if not user_notes:
        return {
            "id": None,
            "word_id": word_id,
            "custom_meaning": None,
            "custom_sentence_1": None,
            "custom_sentence_2": None,
        }
    
    return {
        "id": str(user_notes.id),
        "word_id": str(word_id),
        "custom_meaning": user_notes.custom_meaning,
        "custom_sentence_1": user_notes.custom_sentence_1,
        "custom_sentence_2": user_notes.custom_sentence_2,
        "updated_at": user_notes.updated_at.isoformat(),
    }
