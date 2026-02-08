# Quick Start Guide

Get the SAT Vocabulary Learning App running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (or use Docker)
- OpenAI API key

## Option 1: Docker Compose (Recommended)

1. **Clone and navigate to project:**
```bash
cd satquiz
```

2. **Set up environment variables:**
```bash
# Backend
cd backend
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Frontend
cd ../frontend
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

3. **Start all services:**
```bash
cd ..
docker-compose up -d
```

4. **Initialize database:**
```bash
docker-compose exec backend python init_db.py
```

5. **Access the app:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Option 2: Local Development

### Backend Setup

1. **Navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your configuration:
# - DATABASE_URL
# - OPENAI_API_KEY
```

5. **Set up database:**
```bash
# Create database
createdb satquiz

# Initialize tables
python init_db.py
# OR use Alembic:
# alembic upgrade head
```

6. **Run server:**
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment:**
```bash
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

4. **Run development server:**
```bash
npm run dev
```

## First Steps

1. **Login:**
   - Go to http://localhost:5173
   - Enter your email (for development)
   - In production, this would use Google OAuth

2. **Upload a PDF:**
   - Navigate to "Upload PDF" page
   - Upload a PDF with SAT vocabulary words
   - The system will extract words and generate meanings

3. **Browse Words:**
   - View all words on the dashboard
   - Click on a word to see details
   - Add words to favorites
   - Edit notes and meanings

## Troubleshooting

### Database Connection Error
- Make sure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `psql -l | grep satquiz`

### OpenAI API Error
- Verify OPENAI_API_KEY is set in .env
- Check your OpenAI account has credits

### Frontend Can't Connect to Backend
- Verify backend is running on port 8000
- Check VITE_API_URL in frontend/.env
- Check CORS settings in backend/app/main.py

### PDF Upload Not Working
- Make sure file is a valid PDF
- Check backend logs for errors
- Verify S3 credentials if using AWS

## Next Steps

- Read [README.md](./README.md) for detailed documentation
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for AWS deployment
- Review API documentation at http://localhost:8000/docs
