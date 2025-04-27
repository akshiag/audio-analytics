# tests/test_db.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import get_db, get_db_commit

# Create a test SQLite engine (memory database)
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Fixture to create and teardown a database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_db(db_session):
    """Test that get_db yields a working session."""
    gen = get_db()
    session = next(gen)
    assert session is not None
    session.close()

def test_get_db_commit(db_session):
    """Test that get_db_commit yields a working session."""
    gen = get_db_commit()
    session = next(gen)
    assert session is not None
    session.close()
