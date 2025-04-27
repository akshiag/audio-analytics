import time
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.asr_service import transcribe
from app.audio_utils import get_audio_duration
from app.models import Transcription
from app.schemas import AnalyzeResponse


async def process_audio_and_save(db: Session, file_path: str) -> AnalyzeResponse:
    """
    Transcribe an audio file and save it to the database.

    Args:
        db (Session): SQLAlchemy database session.
        file_path (str): Path to the audio file.

    Returns:
        AnalyzeResponse: Contains text, processing_time, and audio_duration.
    """
    start_time = time.time()

    transcription_result = await transcribe(file_path)
    text = transcription_result["text"]

    processing_time = round(time.time() - start_time, 2)
    audio_duration = get_audio_duration(file_path)

    # Reuse save_transcription function
    save_transcription(
        db=db,
        text=text,
        audio_duration=audio_duration,
        processing_time=processing_time
    )

    return AnalyzeResponse(
        text=text,
        processing_time=processing_time,
        audio_duration=audio_duration
    )


def save_transcription(
    db: Session,
    text: str,
    audio_duration: float,
    processing_time: float
) -> None:
    """
    Save a transcription record to the database.

    Args:
        db (Session): SQLAlchemy database session.
        text (str): The transcribed text from the audio file.
        audio_duration (float): The duration of the audio file in seconds.
        processing_time (float): The time taken to process the transcription in seconds.
    """
    transcription = Transcription(
        text=text,
        audio_duration=audio_duration,
        processing_time=processing_time,
        created_at=datetime.now(timezone.utc)
    )

    db.add(transcription)
