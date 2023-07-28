# config.py
from dotenv import load_dotenv
import os
from elevenlabs import set_api_key
import openai

def configure_environment():
    load_dotenv()

    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY is not set or is empty!")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set or is empty!")

    set_api_key(elevenlabs_api_key)
    openai.api_key = openai_api_key

