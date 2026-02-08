# SAT Vocabulary Backend API

FastAPI backend for the SAT Vocabulary Learning App.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   │   ├── auth.py   # Authentication
│   │   ├── words.py  # Word endpoints
│   │   ├── favorites.py
│   │   ├── notes.py
│   │   └── upload.py
│   ├── models/       # SQLAlchemy models
│   ├── services/     # Business logic
│   │   ├── llm_service.py
│   │   ├── pdf_parser.py
│   │   └── word_service.py
│   └── db/           # Database configuration
├── worker/           # Background worker
├── alembic/          # Database migrations
└── requirements.txt
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key for LLM generation
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region
- `S3_BUCKET` - S3 bucket for PDF storage
- `SQS_QUEUE_URL` - SQS queue URL for background processing

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## Testing

```bash
pytest
```

## Docker

Build image:
```bash
docker build -t satquiz-api .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env satquiz-api
```
