import openai
from dotenv import load_dotenv
import os
import asyncio

from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate

import record_and_translate
from dotenv import load_dotenv
import os
from elevenlabs import set_api_key, generate, play

load_dotenv()

eleven_labs_key = os.getenv('ELEVENLABS_API_KEY')
set_api_key(eleven_labs_key)

# load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def input_to_chain(ConvoChain:ConversationChain,text_input:str):
    return ConvoChain(text_input)

def play_text(text, voice="Bella", model="eleven_monolingual_v1") -> None:
        audio = generate(
        text=text,
        voice=voice,
        model=model
        )

        play(audio)



llm = OpenAI(model_name='text-davinci-003', 
             temperature=0, 
             max_tokens = 256)

system_prompt = template = """"You are a game master for a Zork-style game. You must keep track of the user's game states, 
and provide a fun and challenging experience. Zork is a classic text-based adventure game, 
assist in generating text-based responses and managing the game's logic.

{history}

Conversation:
Human: {input}
AI:
"""

prompt = PromptTemplate(
    input_variables=["history", "input"], template=template
)

conversation_with_kg = ConversationChain(
    llm=llm, 
    verbose=True, 
    prompt=prompt,
    memory=ConversationKGMemory(llm=llm)
)



# convo = []
# current_text = input_to_chain(conversation_with_kg, "Where am i ")
# print(current_text['response'])
# convo.append(current_text)

# while current_text != 'end': 
#     current_text = input()
#     current_chain = input_to_chain(conversation_with_kg,current_text)
#     convo.append(current_chain)
#     print(current_chain['response'])


async def main():
    async with record_and_translate.MonocleAudioServer() as audio_server:
        convo = []
        current_text = input_to_chain(conversation_with_kg, "Where am i ")

        current_response = current_text['response']

        audio = generate(
        text=current_response,
        voice="Bella",
        model="eleven_monolingual_v1"
        )

        play(audio)


        print(current_text['response'])
        convo.append(current_text)

        # data = ""
        while current_text != "end game":
            await audio_server.send_payload()
            audio_server.write_audio()
            current_text = record_and_translate.transcribe(record_and_translate.AUDIO_OUTPUT_PATH,"medium")
            print(current_text)
            current_chain = input_to_chain(conversation_with_kg,current_text)
            convo.append(current_chain)
            print(current_chain['response'])

            current_response = current_chain['response']

            audio = generate(
            text=current_response,
            voice="Bella",
            model="eleven_monolingual_v1"
            )

            play(audio)


        # while current_text != 'end': 
        #     current_text = input()
        #     current_chain = input_to_chain(conversation_with_kg,current_text)
        #     convo.append(current_chain)
        #     print(current_chain['response'])


if __name__ == "__main__":
    asyncio.run(main())

x=0