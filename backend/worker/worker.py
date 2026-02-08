"""
Background worker service for processing words from SQS.
In production, this would run as a separate service (ECS task or Lambda).
"""
import os
import json
import boto3
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.db.database import SessionLocal
from app.services.word_service import create_word_with_llm
from app.models.word import Word

load_dotenv()

# SQS configuration
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def process_word_from_queue():
    """
    Poll SQS queue for word processing jobs and process them.
    In production, this would run continuously.
    """
    if not SQS_QUEUE_URL:
        print("SQS_QUEUE_URL not configured. Skipping queue processing.")
        return
    
    db: Session = SessionLocal()
    
    try:
        # Receive messages from SQS
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,  # Long polling
        )
        
        messages = response.get("Messages", [])
        
        for message in messages:
            try:
                body = json.loads(message["Body"])
                word_text = body.get("word")
                source = body.get("source", "pdf")
                
                if not word_text:
                    print(f"Invalid message: {body}")
                    continue
                
                # Check if word already exists
                existing = db.query(Word).filter(Word.word == word_text.lower()).first()
                if existing:
                    print(f"Word {word_text} already exists")
                    # Delete message from queue
                    sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"],
                    )
                    continue
                
                # Create word with LLM generation
                import asyncio
                word = asyncio.run(create_word_with_llm(db, word_text, source))
                print(f"Created word: {word.word} (ID: {word.id})")
                
                # Delete message from queue after successful processing
                sqs_client.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"],
                )
                
            except Exception as e:
                print(f"Error processing message: {e}")
                # In production, you might want to send to DLQ after retries
                continue
    
    except Exception as e:
        print(f"Error receiving messages: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting word processing worker...")
    while True:
        process_word_from_queue()
