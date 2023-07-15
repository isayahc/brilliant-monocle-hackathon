import whisper 

def speech_to_text(model_type="base",input_data="output.mp3") -> str:
    model = whisper.load_model(model_type)
    result = model.transcribe(input_data)
    return (result["text"])