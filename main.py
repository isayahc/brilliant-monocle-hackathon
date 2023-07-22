from dotenv import load_dotenv
import os
import asyncio

from elevenlabs import set_api_key
import openai

from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain

import monocial_utils
import utils
import llm_chain

# Load environemnt variables
load_dotenv()

# Configuring API keys
set_api_key(os.getenv('ELEVENLABS_API_KEY'))
openai.api_key = os.getenv('OPENAI_API_KEY')

async def generate_and_play_response(text):
    response = llm_chain.input_to_chain(conversation_with_kg, text)
    utils.generate_and_play_speech(response['response'])
    return response

async def handle_conversation_turn(audio_server):
    await audio_server.send_payload()
    audio_server.write_audio()
    transcribed_text = utils.transcribe(monocial_utils.AUDIO_OUTPUT_PATH, "medium")
    return await generate_and_play_response(transcribed_text)

async def conversation_loop(audio_server):
    convo = []
    initial_text = "Where am I"
    response = await generate_and_play_response(initial_text)
    convo.append(response)
    while response['input'] != "end game":
        response = await handle_conversation_turn(audio_server)
        convo.append(response)
    return convo

async def main():
    async with monocial_utils.MonocleAudioServer() as audio_server:
        convo = await conversation_loop(audio_server)

if __name__ == "__main__":
    llm = OpenAI(model_name='text-davinci-003', temperature=0, max_tokens=256)

    system_prompt = """
    You are a game master for a Zork-style game. You must keep track of the user's game states, 
    and provide a fun and challenging experience. Zork is a classic text-based adventure game, 
    assist in generating text-based responses and managing the game's logic.

    {history}

    Conversation:
    Human: {input}
    AI:
    """

    prompt = PromptTemplate(
        input_variables=["history", "input"], 
        template=system_prompt
    )

    conversation_with_kg = ConversationChain(
        llm=llm, 
        verbose=True, 
        prompt=prompt,
        memory=ConversationKGMemory(llm=llm)
    )

    asyncio.run(main())
