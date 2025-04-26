import tempfile
import time

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session

from app.asr_service import transcribe
from app.audio_utils import get_audio_duration
from app.db import engine, get_db, get_db_commit
from app.models import Base
from app.schemas import AnalyzeResponse, StatsResponse
from app.services.stats_service import get_statistics
from app.services.transcription_service import save_transcription

load_dotenv()  # Load environment variables from a .env file

# Initialize the FastAPI application
app = FastAPI(
    title="Audio to Text Microservice",
    version="1.0.0"
)

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# --- Routes ---

@app.get("/", tags=["Landing"])
async def root() -> dict:
    """
    Landing page of the Audio to Text Microservice.

    Returns:
        dict: A welcome message and available endpoints.
    """
    return {
        "message": "Welcome to the Audio to Text Microservice!",
        "available_endpoints": {
            "POST /analyze": "Upload an audio file and receive transcription",
            "GET /stats": "View transcription statistics",
            "Docs": "/docs (Swagger UI)"
        }
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_audio(file: UploadFile = File(...),
                        db: Session = Depends(get_db_commit)) -> AnalyzeResponse:
    """
    Analyze an uploaded audio file and return its transcription, processing time, and duration.

    Args:
        file (UploadFile): The uploaded audio file.
        db (Session): SQLAlchemy database session.

    Returns:
        AnalyzeResponse: The transcription, processing time, and audio duration.
    """
    # Create a temporary file to store the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path: str = tmp.name

    # Measure the start time for processing
    start_time: float = time.time()

    # Transcribe the audio file
    transcription_result: dict = await transcribe(tmp_path)
    text: str = transcription_result["text"]

    # Calculate processing time and audio duration
    processing_time: float = round(time.time() - start_time, 2)
    audio_duration: float = get_audio_duration(tmp_path)

    # Save the transcription details to the database
    save_transcription(db=db, text=text, audio_duration=audio_duration,
                       processing_time=processing_time)

    # Return the transcription details
    return AnalyzeResponse(
        text=text,
        processing_time=processing_time,
        audio_duration=audio_duration
    )

@app.get("/stats", response_model=StatsResponse)
async def stats(db: Session = Depends(get_db)) -> StatsResponse:
    """
    Retrieve statistics about the transcriptions stored in the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        StatsResponse: Statistics including total calls, median latency, and median audio length.
    """
    return get_statistics(db)