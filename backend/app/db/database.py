import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from backend/.env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

# Read the database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")


# Create the database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for database models
class Base(DeclarativeBase):
    pass


# Test database connectivity
def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful:", result.scalar())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
