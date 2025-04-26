from pydantic import BaseModel, Field


class AnalyzeResponse(BaseModel):
    """
    Represents the response for an audio analysis request.

    Attributes:
        text (str): The transcribed text from the audio file.
        processing_time (float): The time taken to process the request, in seconds.
        audio_duration (float): The duration of the uploaded audio file, in seconds.
    """
    text: str = Field(..., description="Transcribed text from the audio file")
    processing_time: float = Field(..., description="Time taken to process the request, "
                                                    "in seconds")
    audio_duration: float = Field(..., description="Duration of the uploaded audio file, "
                                                   "in seconds")


class StatsResponse(BaseModel):
    """
    Represents the response for transcription statistics.

    Attributes:
        total_calls (int): Total number of transcription API calls.
        median_latency (float): Median processing latency across all calls, in seconds.
        median_audio_length (float): Median audio length across all calls, in seconds.
    """
    total_calls: int = Field(..., description="Total number of transcription API calls")
    median_latency: float = Field(..., description="Median processing latency across all calls,"
                                                   " in seconds")
    median_audio_length: float = Field(..., description="Median audio length across all calls,"
                                                        " in seconds")
