from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.word import Word
from app.api.auth import get_current_user
from app.models.user import User
from app.services.pdf_parser import extract_words_from_pdf
from app.services.word_service import create_word_with_llm
import boto3
import os
from dotenv import load_dotenv
from typing import List
from io import BytesIO

load_dotenv()

router = APIRouter()

# S3 configuration
S3_BUCKET = os.getenv("S3_BUCKET", "satquiz-pdfs")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a PDF file, extract words, and trigger background processing.
    In production, this would upload to S3 and trigger a Lambda/SQS workflow.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Read file content
    content = await file.read()
    
    # Extract words from PDF
    try:
        words_list = extract_words_from_pdf(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing PDF: {str(e)}")
    
    if not words_list:
        raise HTTPException(status_code=400, detail="No words found in PDF")
    
    # Upload to S3 (if configured)
    s3_key = None
    if os.getenv("AWS_ACCESS_KEY_ID"):
        try:
            s3_key = f"uploads/{current_user.id}/{file.filename}"
            s3_client.upload_fileobj(
                BytesIO(content),
                S3_BUCKET,
                s3_key,
            )
        except Exception as e:
            print(f"Warning: Could not upload to S3: {e}")
    
    # In production, you would:
    # 1. Upload PDF to S3
    # 2. Send words to SQS queue
    # 3. Worker processes words asynchronously
    
    # For now, we'll process words synchronously (not ideal for production)
    # In production, return immediately and process via SQS worker
    processed_words = []
    errors = []
    
    for word_text in words_list[:10]:  # Limit to 10 for demo
        try:
            # Check if word already exists
            existing = db.query(Word).filter(Word.word == word_text.lower()).first()
            if existing:
                processed_words.append({"word": word_text, "status": "exists"})
                continue
            
            # Create word with LLM generation
            word = await create_word_with_llm(db, word_text, source="pdf")
            processed_words.append({"word": word_text, "status": "created", "id": str(word.id)})
        except Exception as e:
            errors.append({"word": word_text, "error": str(e)})
    
    return {
        "message": f"Processed {len(processed_words)} words",
        "total_words_found": len(words_list),
        "processed": processed_words,
        "errors": errors,
        "s3_key": s3_key,
    }
