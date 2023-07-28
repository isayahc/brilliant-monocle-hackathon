# conversation.py
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationKGMemory
import utils
import monocle_utils


def input_to_chain(ConvoChain: ConversationChain, text_input: str) -> ConversationChain:
    """
    Feed the input text into the conversation chain.

    :param ConvoChain: The conversation chain to use.
    :param text_input: The input text.
    :return: The updated conversation chain.
    """
    return ConvoChain(text_input)

def create_conversation_chain():
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

    prompt = PromptTemplate(template=system_prompt)

    conversation_with_kg = ConversationChain(
        llm=llm, 
        verbose=True, 
        prompt=prompt,
        memory=ConversationKGMemory(llm=llm)
    )

    return conversation_with_kg

async def generate_and_play_response(conversation_with_kg:ConversationChain, text:str):
    response = input_to_chain(conversation_with_kg, text)
    utils.generate_and_play_speech(response['response'])
    return response

async def handle_conversation_turn(audio_server:monocle_utils.MonocleAudioServer, model_size:str, conversation_with_kg:ConversationChain):
    await audio_server.send_payload()
    audio_server.write_audio()
    transcribed_text = utils.transcribe(monocle_utils.AUDIO_OUTPUT_PATH, model_size)
    return await generate_and_play_response(conversation_with_kg, transcribed_text)

async def conversation_loop(audio_server:monocle_utils.MonocleAudioServer, model_size:str, conversation_with_kg:ConversationChain):
    convo = []
    initial_text = "Where am I"
    response = await generate_and_play_response(conversation_with_kg, initial_text)
    convo.append(response)
    while response['input'] != "end game":
        response = await handle_conversation_turn(audio_server, model_size, conversation_with_kg)
        convo.append(response)
    return convo
