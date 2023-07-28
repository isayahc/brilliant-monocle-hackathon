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
import config




async def generate_response(text):
    response = llm_chain.input_to_chain(conversation_with_kg, text)
    return response

async def handle_conversation_turn(model_size):
    transcribed_text = input("Enter your input: ")  # Here we use standard input instead of transcribing from audio.
    return await generate_response(transcribed_text)

async def conversation_loop(model_size):
    convo = []
    initial_text = "Where am I"
    response = await generate_response(initial_text)
    print(response)
    convo.append(response)
    while response['input'] != "end game":
        response = await handle_conversation_turn(model_size)
        print(response)
        convo.append(response)
    return convo

async def main(model_size):
    convo = await conversation_loop(model_size)

if __name__ == "__main__":
    config.configure_environment()
    llm = OpenAI(model_name='text-davinci-003', temperature=0, max_tokens=256)

    system_prompt = """
    You are a game master for a Zork-style game. You must keep track of the user's game states, 
    and provide a fun and challenging experience. Zork is a classic text-based adventure game, 
    assist in generating text-based responses and managing the game's logic. If the play makes an invalid choice make sure to remind them where they are

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

    model_size = "medium"
    asyncio.run(main(model_size))
