import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import get_db, get_db_commit
from app.main import app
from app.models import Base, Transcription

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_db_commit] = override_get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        for tbl in reversed(Base.metadata.sorted_tables):
            db.execute(tbl.delete())
        db.commit()
        db.close()

def test_landing_page():
    """Test landing page returns welcome message and available endpoints."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert "available_endpoints" in data
    assert data["message"].startswith("Welcome to the Audio to Text Microservice")
    assert "POST /analyze" in data["available_endpoints"]
    assert "GET /stats" in data["available_endpoints"]
    assert "Swagger Docs" in data["available_endpoints"]

def test_stats_empty_database(db_session):
    """Test stats endpoint returns 0 when there are no transcriptions."""
    stats_response = client.get("/stats")
    assert stats_response.status_code == 200
    stats = stats_response.json()

    assert stats["total_calls"] == 0
    assert stats["median_latency"] == 0
    assert stats["median_audio_length"] == 0


def test_stats_with_known_insertions(db_session):
    """Insert known transcriptions and check exact stats."""
    transcriptions = [
        Transcription(text="test1", audio_duration=10.0, processing_time=0.5),
        Transcription(text="test2", audio_duration=20.0, processing_time=0.7),
        Transcription(text="test3", audio_duration=30.0, processing_time=0.9),
    ]
    db_session.add_all(transcriptions)
    db_session.commit()

    stats_response = client.get("/stats")
    assert stats_response.status_code == 200
    stats = stats_response.json()

    assert stats["total_calls"] == 3
    assert stats["median_latency"] == 0.7
    assert stats["median_audio_length"] == 20.0


def test_analyze_with_sample_audio(db_session):
    """Upload sample audio file to /analyze and check the output."""

    sample_audio_path = "tests/resources/harvard.wav"
    assert os.path.exists(sample_audio_path), "Sample audio file not found!"

    # Step 1: Upload the file
    with open(sample_audio_path, "rb") as f:
        files = {"file": ("harvard.wav", f, "audio/wav")}
        response = client.post("/analyze", files=files)

    assert response.status_code == 200

    # Step 2: Validate response
    data = response.json()

    text = data.get("text", "").strip()

    expected_keywords = [
        "stale smell of old beer",
        "cold dip restores health",
        "salt pickle tastes fine with ham",
        "tacos all pastora",
        "zestful food is the hot cross bun"
    ]

    for phrase in expected_keywords:
        assert phrase in text.lower(), f"Phrase '{phrase}' not found in transcription"

    assert isinstance(data["processing_time"], float)
    assert data["processing_time"] <= 1.5

    assert isinstance(data["audio_duration"], float)
    expected_audio_duration = 18.356
    assert abs(data["audio_duration"] - expected_audio_duration) <= 0.5

