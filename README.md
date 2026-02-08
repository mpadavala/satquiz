# SAT Vocabulary Learning App

A full-stack application for learning SAT vocabulary words with AI-generated meanings and example sentences.

## Architecture

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Storage**: AWS S3
- **Background Jobs**: AWS SQS
- **LLM**: OpenAI API
- **Auth**: AWS Cognito (Google OAuth)

## Project Structure

```
satquiz/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── models/   # Database models
│   │   ├── services/ # Business logic
│   │   └── db/       # Database configuration
│   ├── worker/       # Background worker
│   └── alembic/      # Database migrations
├── frontend/         # React frontend
│   └── src/
│       ├── pages/    # Page components
│       ├── components/ # Reusable components
│       ├── api/      # API client
│       └── hooks/    # React hooks
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up database:
```bash
# Create database
createdb satquiz

# Run migrations
alembic upgrade head
```

6. Run the server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

4. Run development server:
```bash
npm run dev
```

## Features

### Student Features
- ✅ Login with Google (OAuth)
- ✅ View SAT vocabulary word list
- ✅ See word meanings and example sentences
- ✅ Favorite words
- ✅ Save custom notes/edited meanings/sentences
- ✅ Upload SAT wordlist PDF → auto-parse → add words to DB

### Admin Features
- ✅ Upload word list PDFs
- ✅ Trigger LLM generation for new words

## API Endpoints

### Auth
- `GET /api/me` - Get current user

### Words
- `GET /api/words` - List all words
- `GET /api/words/{id}` - Get word detail
- `POST /api/favorite/{word_id}` - Toggle favorite
- `GET /api/favorites` - Get user favorites

### Notes
- `GET /api/notes/{word_id}` - Get notes for word
- `PUT /api/notes/{word_id}` - Update notes

### Upload
- `POST /api/upload-pdf` - Upload PDF file

## Database Schema

- `users` - User accounts
- `words` - Vocabulary words
- `user_favorites` - User favorite words
- `user_notes` - User custom notes

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed AWS deployment instructions.

## Development

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## License

MIT
