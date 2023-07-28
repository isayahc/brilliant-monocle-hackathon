from typing import Callable
import wave

import whisper
from elevenlabs import generate, play


def transcribe(
        fp: str,
        model_size: str = "base"
        ) -> str:
    """
    Transcribe audio from a file using a model from the Whisper ASR (Automatic Speech Recognition) system.

    :param fp: Filepath to the audio file to transcribe.
    :param model_size: Size of the Whisper ASR model to use. Default is "base".
    :return: The transcribed text.
    """
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        print(f"Error loading model: {e}")
        return ""

    try:
        result = model.transcribe(fp)
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

    transcript = result.get("text", "")
    
    return transcript


def generate_and_play_speech(
        text: str, 
        voice: str="Bella", 
        model: str="eleven_monolingual_v1"
        ) -> None:
    """
    Generate speech audio from text and play it.

    :param text: Text to generate speech from.
    :param voice: Voice to use for speech generation. Default is "Bella".
    :param model: Model to use for speech generation. Default is "eleven_monolingual_v1".
    """
    try:
        audio = generate(text=text, voice=voice, model=model)
    except Exception as e:
        print(f"Error generating audio: {e}")
        return

    try:
        play(audio)
    except Exception as e:
        print(f"Error playing audio: {e}")


def generate_speech(
        text: str, 
        voice: str="Bella", 
        model: str="eleven_monolingual_v1"
        ) -> bytes:
    """
    Generate speech audio from text and return it.

    :param text: Text to generate speech from.
    :param voice: Voice to use for speech generation. Default is "Bella".
    :param model: Model to use for speech generation. Default is "eleven_monolingual_v1".
    :return: The generated speech audio.
    """
    try:
        audio = generate(
            text=text, 
            voice=voice, 
            model=model
            )
    except Exception as e:
        print(f"Error generating audio: {e}")
        return b""

    return audio


def do_something_with_generated_audio(
    generate_func, 
    play_func, 
    text, 
    voice="Bella", 
    model="eleven_monolingual_v1"
) -> None:

    audio = generate_func(
        text=text,
        voice=voice,
        model=model
    )

    play_func(audio)


def save_bytes_to_wav(
    byte_data: bytes, 
    filename: str, 
    nchannels: int = 1, 
    sampwidth: int = 2, 
    framerate: int = 44100
) -> None:

    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(nchannels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(framerate)
        wav_file.writeframes(byte_data)


def save_conversation_as_txt(convo):
    """
    Save the conversation history as a .txt file.

    :param convo: The conversation history as a sequence of responses.
    :type convo: List[dict]
    """
    # Create a filename for the .txt file (you can customize the filename as needed).
    filename = "conversation_history.txt"

    with open(filename, "w", encoding="utf-8") as file:
        for response in convo:
            input_text = response.get('input', '')
            output_text = response.get('response', '')

            # Write each input and output text to the .txt file.
            file.write(f"User: {input_text}\n")
            file.write(f"Bot: {output_text}\n\n")
