import whisper
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the Whisper model
model = whisper.load_model("small")

def safe_transcribe(path):
    """
    Attempts to transcribe the audio from the given path using the Whisper model.
    In case of an error, it logs the error and returns an appropriate message.

    :param path: Path to the audio file to be transcribed.
    :return: Dictionary with transcription result or error message.
    """
    try:
        # Attempt to transcribe
        return model.transcribe(path, language="en")
    except Exception as e:
        # Log the error instead of printing
        logger.error(f"Error transcribing {path}: {e}")
        # Return a dictionary with the error message
        return {"error": f"Error transcribing {path}: {e}"}