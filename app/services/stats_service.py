import statistics

from sqlalchemy.orm import Session

from app.models import Transcription
from app.schemas import StatsResponse


def get_statistics(db: Session) -> StatsResponse:
    """
    Retrieve transcription statistics from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        StatsResponse: Object containing total_calls, median_latency, median_audio_length.
    """

    # Query all transcription records from the database
    transcriptions = db.query(Transcription).all()
    total_calls = len(transcriptions)  # Total number of transcription records

    # If no transcriptions exist, return default statistics
    if total_calls == 0:
        return StatsResponse(
            total_calls=0,
            median_latency=0,
            median_audio_length=0
        )

    # Extract processing times and audio durations from the transcriptions
    latencies = [t.processing_time for t in transcriptions]
    durations = [t.audio_duration for t in transcriptions]

    # Calculate the median processing time and median audio duration
    median_latency = round(statistics.median(latencies), 2)
    median_audio_length = round(statistics.median(durations), 2)

    # Return the calculated statistics as a StatsResponse object
    return StatsResponse(
        total_calls=total_calls,
        median_latency=median_latency,
        median_audio_length=median_audio_length
    )