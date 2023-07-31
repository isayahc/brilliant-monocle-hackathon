import json
from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory.chat_memory import ChatMemory 
from langchain.schema import ChatMessage
from pathlib import Path

# For typing
from langchain.chains import ConversationChain
from langchain.schema import ChatMessage
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory import chat_memory

from config import configure_environment
import config_handler

def setup_conversation_chain(conversation_save_path:str, config):
    model_size = config.get("model_size", "medium")
    model_name = config.get("model_name", "text-davinci-003")
    temperature = config.get("temperature", 0)
    max_tokens = config.get("max_tokens", 256)

    llm = OpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)

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
        
    return llm, prompt

def load_conversation(
        conversation_save_path, 
        llm, 
        prompt
        ) -> ConversationChain:
    with open(conversation_save_path, 'r') as file:
        loaded_data = json.load(file)
        loaded_data = json.loads(loaded_data)

    retrieved_memory = ConversationBufferMemory(chat_memory=loaded_data)
    conversation_with_kg = ConversationChain(
        llm=llm,
        verbose=True,
        memory=retrieved_memory,
        prompt=prompt
    )

    message_list = [ChatMessage(text=i['text'],role=i['role']) for i in loaded_data['messages']]
    conversation_with_kg.memory.chat_memory.messages = message_list

    return conversation_with_kg

def new_conversation(llm, prompt):
    conversation_with_kg = ConversationChain(
        llm=llm, 
        verbose=True, 
        prompt=prompt,
        memory=ConversationKGMemory(llm=llm)
    )
    return conversation_with_kg

def save_conversation(
        conversation_with_kg: ConversationChain, 
        conversation_save_path:str
        ) -> None:
    with open(conversation_save_path, 'w') as file:
        json.dump(conversation_with_kg.memory.chat_memory.json(), file)

def extract_langchain_messages(
        conversation_with_kg: ConversationChain
        ) -> list[ChatMessage]:
    return conversation_with_kg.chat_memory.messages

def initalize_conversation_loop(
        conversation_with_kg: ConversationChain
        ) -> ConversationChain:
    """
    Run the conversation loop, where the conversation chain interacts with the user in a back-and-forth manner.

    :param audio_server: The MonocleAudioServer to receive audio input.
    :type audio_server: monocle_utils.MonocleAudioServer
    :param model_size: The size of the model used for transcription.
    :type model_size: str
    :param conversation_with_kg: The conversation chain to use.
    :type conversation_with_kg: ConversationChain
    :return: ConversationChain
    :rtype: ConversationChain
    """

    chat_logs = conversation_with_kg.memory.chat_memory.messages

    # if chat_logs is empty then this is assumed to be a new ConversationChain object
    if not chat_logs:

        # initialize the chat
        initial_input = "where am i?"

        conversation_with_kg(initial_input)


    return conversation_with_kg


def interact_and_save(
        conversation_with_kg:ConversationChain, 
        conversation_save_path:str
        ) -> None:


    conversation_with_kg = initalize_conversation_loop(conversation_with_kg)
    inital_reponse =  conversation_with_kg.memory.chat_memory.messages[-1].text
    print(inital_reponse)

    user_input = input("what would you like to do?")
    while user_input != "end":
        response = conversation_with_kg(user_input)['response']
        print(response)
        user_input = input("what would you like to do?")

    save_conversation(conversation_with_kg, conversation_save_path)

def input_to_chain(
        conversation_chain: ConversationChain, 
        text_input: str
        ) -> ConversationChain:
    """
    Feed the input text into the conversation chain.

    :param conversation_chain: The conversation chain to use.
    :type conversation_chain: ConversationChain
    :param text_input: The input text to be processed by the conversation chain.
    :type text_input: str
    :return: The updated conversation chain after processing the input text.
    :rtype: ConversationChain
    """
    return conversation_chain(text_input)



if __name__ == "__main__":
    configure_environment()
    config_location = "config.json"

    if config_handler.config_exists(config_location):
        config = config_handler.load_config(config_location)

    if config is None:
        exit(1)

    conversation_save_path = config.get("conversation_save_path", "")

    llm, prompt = setup_conversation_chain(conversation_save_path, config)
    
    if Path(conversation_save_path).exists():
        conversation_with_kg = load_conversation(conversation_save_path, llm, prompt)
    else:
        conversation_with_kg = new_conversation(llm, prompt)

    interact_and_save(conversation_with_kg, conversation_save_path)

