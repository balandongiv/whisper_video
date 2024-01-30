import whisper

model = whisper.load_model("small")




def safe_transcribe(path):
    try:
        # Attempt to transcribe
        return model.transcribe(path, language="en")
    except Exception as e:
        # If transcription fails, handle the exception
        print(f"Error transcribing {path}: {e}")
        return f"Error transcribing {path}: {e}"