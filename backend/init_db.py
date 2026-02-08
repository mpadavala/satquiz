"""
Initialize the database with tables.
Run this script to create all tables without using Alembic.
"""
from app.db.database import engine, Base
from app.models import User, Word, UserFavorite, UserNotes

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
