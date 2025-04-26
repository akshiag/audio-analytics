from faster_whisper import WhisperModel

# Load the model once at startup
# Currently using the 'tiny' model optimized for CPU.
# To improve transcription quality or speed:
# - Use 'small', 'base', or larger models
# - Switch 'device' to 'cuda' for GPU acceleration
model = WhisperModel(
    model_size_or_path="tiny",
    device="cpu",
    compute_type="int8"
)

# The `async` keyword is used to define an asynchronous function.
# Asynchronous functions allow non-blocking execution, means function can perform I/O-bound tasks
# (like file operations or network requests) without blocking the main thread.
# This is particularly useful in web applications to handle multiple requests concurrently.

async def transcribe(file_path: str) -> dict:
    """
    Transcribe an audio file to text using the Whisper model.

    Args:
        file_path (str): The path to the audio file.

    Returns:
        dict: A dictionary containing the transcribed text.
    """
    # Transcribe the audio file using the Whisper model.
    # The `model.transcribe` method processes the audio file and returns segments and metadata.
    segments, info = model.transcribe(file_path)

    # Combine the text from all segments into a single string.
    # Each segment contains a portion of the transcribed text.
    text = " ".join(str(segment.text) for segment in segments)  # Ensure type casting to string

    # Return the transcribed text as a dictionary.
    return {"text": text}