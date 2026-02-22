import whisper

def transcribe_audio(audio_path, model_size="tiny"):
    """
    Transcribe audio file using Whisper.
    Returns transcript as string.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]