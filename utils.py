import whisper
from elevenlabs import generate, play

def transcribe(fp: str,model_size="base"):
    model = whisper.load_model(model_size)
    # Ideally we would just take in a tensor of the raw audio bytes rather than
    # pass in a path.
    result = model.transcribe(fp)
    transcript = result["text"]
    return transcript

def generate_speech(text, voice="Bella", model="eleven_monolingual_v1") -> None:
        audio = generate(
        text=text,
        voice=voice,
        model=model
        )

        play(audio)

def do_something_with_generated_audio(generate_func, play_func, text, voice="Bella", model="eleven_monolingual_v1") -> None:
    audio = generate_func(
        text=text,
        voice=voice,
        model=model
    )

    play_func(audio)
