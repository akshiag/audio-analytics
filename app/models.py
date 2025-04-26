from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, Text
from sqlalchemy.orm import declarative_base

# Defines the base class for SQLAlchemy models
Base = declarative_base()

class Transcription(Base):
    """
    Represents a transcription record in the database.

    Attributes:
        id (int): Primary key, unique identifier for the transcription.
        text (str): The transcribed text from the audio file.
        audio_duration (float): Duration of the audio file in seconds.
        processing_time (float): Time taken to process the transcription in seconds.
        created_at (datetime): Timestamp when the transcription was created.
    """
    __tablename__ = "transcriptions"

    id: int = Column(Integer, primary_key=True, index=True)
    text: str = Column(Text)
    # Duration of the audio in seconds
    audio_duration: float = Column(Float, comment="Audio duration in seconds")
    # Time taken for processing in seconds
    processing_time: float = Column(Float, comment="Processing time in seconds")
    # Creation timestamp in seconds
    created_at: datetime = Column(DateTime, default=datetime.now(timezone.utc))