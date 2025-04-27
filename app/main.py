import os
import tempfile

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session

from app.db import engine, get_db, get_db_commit  # Database engine and session dependencies
from app.kafka_producer import kafka_task_producer  # Kafka producer for queuing tasks
from app.models import Base  # SQLAlchemy models
from app.schemas import AnalyzeResponse, StatsResponse  # Pydantic schemas for API responses
from app.services.stats_service import get_statistics  # Service to retrieve statistics
from app.services.transcription_service import process_audio_and_save  # Service to process and save transcriptions

# --- Load Environment Variables ---
load_dotenv()  # Load environment variables from a .env file

# --- Settings ---
# Check if Kafka is enabled via the USE_KAFKA environment variable
USE_KAFKA = os.getenv("USE_KAFKA", "false").lower() == "true"

# --- Initialize FastAPI App ---
# Create a FastAPI application with metadata
app = FastAPI(
    title="Audio to Text Microservice",
    version="1.0.0",
    description="Upload audio files for transcription using Faster-Whisper. "
                "Supports direct processing or Kafka-based queueing."
)

# --- Database Setup ---
# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# --- Routes ---

@app.get("/", tags=["Landing"])
async def root() -> dict:
    """
    Landing page providing basic information and available endpoints.

    Returns:
        dict: A welcome message and available endpoints.
    """
    return {
        "message": "Welcome to the Audio to Text Microservice!",
        "available_endpoints": {
            "POST /analyze": "Upload an audio file and receive transcription",
            "GET /stats": "View transcription statistics",
            "Swagger Docs": "/docs"
        }
    }

@app.post("/analyze", response_model=AnalyzeResponse, tags=["Audio Analysis"])
async def analyze_audio(file: UploadFile = File(...),
                        db: Session = Depends(get_db_commit)) -> AnalyzeResponse:
    """
    Analyzes an uploaded audio file:
    - If Kafka is enabled, the tasks are queued for processing.
    - If not, the transcription is processed immediately.

    Args:
        file (UploadFile): Uploaded audio file.
        db (Session): SQLAlchemy database session.

    Returns:
        AnalyzeResponse: Transcription, processing time, and audio duration.
    """
    # Create a temporary file to store the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())  # Write the uploaded file content to the temporary file
        tmp_path = tmp.name  # Get the path of the temporary file

    if USE_KAFKA:
        # If Kafka is enabled, send the task to the Kafka queue
        kafka_task_producer.send_task({"file_path": tmp_path})
        return AnalyzeResponse(
            text="Task queued for processing.",
            processing_time=0.0,
            audio_duration=0.0
        )

    # If Kafka is not enabled, process the audio file immediately
    result = await process_audio_and_save(db, tmp_path)
    return result

@app.get("/stats", response_model=StatsResponse, tags=["Statistics"])
async def stats(db: Session = Depends(get_db)) -> StatsResponse:
    """
    Retrieve statistics about the transcriptions stored in the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        StatsResponse: Total calls, median latency, and median audio length.
    """
    return get_statistics(db)  # Fetch and return transcription statistics