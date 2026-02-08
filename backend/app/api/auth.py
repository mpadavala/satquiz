from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token.
    In production, this would validate the token with Cognito.
    For now, we'll use a simple email-based approach for development.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # In production, decode and validate JWT from Cognito
    # For development, we'll extract email from a simple token format
    # This should be replaced with proper Cognito JWT validation
    
    # Mock implementation - replace with actual Cognito validation
    email = authorization.replace("Bearer ", "").strip()
    
    # Get or create user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # In production, get user info from Cognito token
        user = User(email=email, name=email.split("@")[0])
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
    }
