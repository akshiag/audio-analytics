from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Transcription


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
