# Local Setup Guide - Step by Step

Follow these steps to run the SAT Vocabulary Learning App on your local machine.

## Prerequisites

Before starting, make sure you have:
- **Python 3.11+** installed (check with `python3 --version`)
- **Node.js 18+** installed (check with `node --version`)
- **PostgreSQL 14+** installed and running (check with `psql --version`)
- **OpenAI API Key** (get one from https://platform.openai.com/api-keys)

## Step 1: Set Up Backend

### 1.1 Navigate to Backend Directory
```bash
cd backend
```

### 1.2 Create Virtual Environment
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 1.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 1.4 Create Environment File
```bash
# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/satquiz
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET=satquiz-pdfs
SQS_QUEUE_URL=
EOF
```

**Important:** Replace `your_openai_api_key_here` with your actual OpenAI API key.

### 1.5 Set Up Database

#### Option A: Using PostgreSQL (if installed locally)
```bash
# Create database
createdb satquiz

# Or using psql:
psql -U postgres
CREATE DATABASE satquiz;
\q
```

#### Option B: Using Docker for PostgreSQL only
```bash
# Run PostgreSQL in Docker
docker run --name satquiz-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=satquiz \
  -p 5432:5432 \
  -d postgres:14
```

### 1.6 Initialize Database Tables
```bash
# Make sure you're in the backend directory with venv activated
python init_db.py
```

This will create all the necessary tables in your database.

## Step 2: Set Up Frontend

### 2.1 Navigate to Frontend Directory
```bash
# From project root
cd frontend
```

### 2.2 Install Node Dependencies
```bash
npm install
```

This may take a few minutes the first time.

### 2.3 Create Environment File
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

## Step 3: Run the Application

You'll need **two terminal windows** - one for backend, one for frontend.

### Terminal 1: Start Backend Server

```bash
# Make sure you're in backend directory with venv activated
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the server
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend Server

```bash
# Make sure you're in frontend directory
cd frontend

# Start the dev server
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 4: Access the Application

1. **Open your browser** and go to: http://localhost:5173

2. **Login Page:**
   - For development, enter any email address (e.g., `test@example.com`)
   - Click "Sign in"
   - You'll be redirected to the dashboard

3. **Test the Application:**
   - Browse words (if any exist)
   - Upload a PDF with vocabulary words
   - View word details
   - Add words to favorites
   - Edit notes

## Step 5: Verify Everything Works

### Check Backend API
- Open http://localhost:8000/docs in your browser
- You should see the Swagger API documentation
- Try the `/health` endpoint

### Check Database Connection
```bash
# Connect to database
psql -U postgres -d satquiz

# List tables
\dt

# Check users table
SELECT * FROM users;

# Exit
\q
```

## Troubleshooting

### Backend Issues

**Problem: Database connection error**
```
Solution: 
1. Make sure PostgreSQL is running: `pg_isready`
2. Check DATABASE_URL in backend/.env
3. Verify database exists: `psql -l | grep satquiz`
```

**Problem: Module not found errors**
```
Solution:
1. Make sure venv is activated (you see (venv) in prompt)
2. Reinstall: `pip install -r requirements.txt`
```

**Problem: OpenAI API errors**
```
Solution:
1. Check OPENAI_API_KEY in backend/.env
2. Verify your OpenAI account has credits
3. Test API key: `curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_KEY"`
```

### Frontend Issues

**Problem: Can't connect to backend**
```
Solution:
1. Make sure backend is running on port 8000
2. Check VITE_API_URL in frontend/.env
3. Check browser console for CORS errors
```

**Problem: npm install fails**
```
Solution:
1. Clear cache: `npm cache clean --force`
2. Delete node_modules: `rm -rf node_modules`
3. Reinstall: `npm install`
```

**Problem: Port 5173 already in use**
```
Solution:
1. Kill process: `lsof -ti:5173 | xargs kill`
2. Or use different port: `npm run dev -- --port 3000`
```

### Database Issues

**Problem: Can't create database**
```
Solution:
1. Make sure PostgreSQL is running
2. Check user permissions: `psql -U postgres -c "SELECT 1"`
3. Create user if needed: `createuser -s postgres`
```

**Problem: Tables not created**
```
Solution:
1. Run: `python init_db.py` from backend directory
2. Or use Alembic: `alembic upgrade head`
```

## Quick Commands Reference

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev

# Database
createdb satquiz
psql -U postgres -d satquiz

# Check if services are running
curl http://localhost:8000/health
curl http://localhost:5173
```

## Next Steps

Once everything is running:
1. Upload a PDF with SAT vocabulary words
2. Browse the extracted words
3. Add words to favorites
4. Edit word notes and meanings
5. Explore the API at http://localhost:8000/docs

## Alternative: Using Docker Compose

If you prefer to use Docker for everything:

```bash
# From project root
docker-compose up -d

# Initialize database
docker-compose exec backend python init_db.py

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

Then access:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
