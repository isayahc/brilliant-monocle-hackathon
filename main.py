from dotenv import load_dotenv
import os

from elevenlabs import set_api_key
import openai


# Load environemnt variables
load_dotenv()


# Configuring API keys
set_api_key(os.getenv('ELEVENLABS_API_KEY'))

openai.api_key = os.getenv('OPENAI_API_KEY')