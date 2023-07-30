import asyncio
import json

from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory.chat_memory import ChatMemory 
from langchain.schema import ChatMessage

import monocle_utils
import conversation
import utils

from config import configure_environment
from pathlib import Path

# Function to load the configuration
def load_config(config_file_path):
    try:
        with open(config_file_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file {config_file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {config_file_path}.")
        return None

# Function to setup a conversation chain
def setup_conversation_chain(conversation_save_path, config):
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
        # input_variables=[],
        template=system_prompt
    )


    if Path(conversation_save_path).exists():
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

    else:
        conversation_with_kg = ConversationChain(
            llm=llm, 
            verbose=True, 
            prompt=prompt,
            memory=ConversationKGMemory(llm=llm)
        )
        
    return conversation_with_kg

# Function to interact with the user
def interact_and_save(conversation_with_kg, conversation_save_path):

    # initialize the conversation 

    chat_logs = conversation_with_kg.memory.chat_memory.messages

    if not chat_logs: 
        initial_input = "where am i?"
        conversation_with_kg(initial_input)
    else:
        last_message = conversation_with_kg.memory.chat_memory.messages[-1].text
        print(last_message)

    data = input()
    while data != "end":
        response = conversation_with_kg(data)
        print(response['response'])
        data = input()


    with open(conversation_save_path, 'w') as file:
        json.dump(conversation_with_kg.memory.chat_memory.json(), file)


if __name__ == "__main__":
    configure_environment()
    config = load_config("config.json")

    if config is None:
        exit(1)

    conversation_save_path = config.get("conversation_save_path", "")
    conversation_with_kg = setup_conversation_chain(conversation_save_path, config)
    interact_and_save(conversation_with_kg, conversation_save_path)
