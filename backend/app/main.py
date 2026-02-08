from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, words, favorites, upload, notes
from app.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SAT Vocabulary API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(words.router, prefix="/api", tags=["words"])
app.include_router(favorites.router, prefix="/api", tags=["favorites"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(notes.router, prefix="/api", tags=["notes"])


@app.get("/")
async def root():
    return {"message": "SAT Vocabulary API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
