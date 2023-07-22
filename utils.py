import whisper 

def transcribe(fp: str,model_size="base"):
    model = whisper.load_model(model_size)
    # Ideally we would just take in a tensor of the raw audio bytes rather than
    # pass in a path.
    result = model.transcribe(fp)
    transcript = result["text"]
    return transcript