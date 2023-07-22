from dotenv import load_dotenv
import os
import asyncio

from elevenlabs import set_api_key
import openai

import monocial_utils
import utils

# Load environemnt variables
load_dotenv()


# Configuring API keys
set_api_key(os.getenv('ELEVENLABS_API_KEY'))

openai.api_key = os.getenv('OPENAI_API_KEY')


async def main():
    async with monocial_utils.MonocleAudioServer() as audio_server:
        convo = []
        current_text = input_to_chain(conversation_with_kg, "Where am i ")

        current_response = current_text['response']


        generate_speech(current_response)


        print(current_text['response'])
        convo.append(current_text)

        while current_text != "end game":

            await audio_server.send_payload()
            audio_server.write_audio()

            current_text = monocial_utils.transcribe(monocial_utils.AUDIO_OUTPUT_PATH,"medium")

            print(current_text)
            current_chain = input_to_chain(conversation_with_kg,current_text)
            convo.append(current_chain)
            
            current_response = current_chain['response']

            print(current_response)

            generate_speech(current_response)

if __name__ == "__main__":
    pass
    # asyncio.run(main())