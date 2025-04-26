import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Detect if the application is running in a testing environment
IS_TESTING: bool = "pytest" in sys.modules

# Set the database URL based on the environment
if IS_TESTING:
    # Use an in-memory SQLite database for testing
    DATABASE_URL: str = "sqlite://"
else:
    # Use the DATABASE_URL environment variable or a default SQLite database file
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./audio_analytics.db")

# Create the SQLAlchemy engine for database connections
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite to allow multithreading
    poolclass=StaticPool if IS_TESTING else None  # Use a static pool for testing
)

# Create a session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency for read-only database operations.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure the session is closed after use

def get_db_commit():
    """
    Dependency for write database operations.

    Yields:
        Session: A SQLAlchemy database session.

    Commits the transaction after use. Rolls back the transaction in case of an error.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Commit the transaction
    except Exception:
        db.rollback()  # Roll back the transaction on error
        raise
    finally:
        db.close()  # Ensure the session is closed after use