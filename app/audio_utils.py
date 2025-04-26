from pydub import AudioSegment  # Library for audio processing


def get_audio_duration(file_path: str) -> float:
    """
    Calculate the duration of an audio file in seconds.

    Args:
        file_path (str): The path to the audio file.

    Returns:
        float: The duration of the audio file in seconds.
    """
    # Load the audio file using pydub
    audio = AudioSegment.from_file(file_path)

    # Calculate the duration in seconds (pydub provides duration in milliseconds)
    duration_seconds = len(audio) / 1000.0
    return duration_seconds