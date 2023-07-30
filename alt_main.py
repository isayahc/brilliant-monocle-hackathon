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

# Define a function to load the configuration
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


if __name__ == "__main__":
    # Use the function to load the configuration
    configure_environment()
    config = load_config("config.json")
    if config is None:
        exit(1)  # Exit if the configuration couldn't be loaded

    # Use the parameters from the configuration in your script
    model_size = config.get("model_size", "medium")  # Use a default value if the key is not present
    model_name = config.get("model_name", "text-davinci-003")
    temperature = config.get("temperature", 0)
    max_tokens = config.get("max_tokens", 256)
    conversation_save_path = config.get("conversation_save_path", "")

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


    data = ""


    if conversation_save_path:
        # Load the dictionary from the JSON file
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

        # load messages into Conversation chain
        message_list = []
        for i in loaded_data['messages']:
            temp = ChatMessage(text=i['text'],role=i['role'])
            message_list.append(temp)

        conversation_with_kg.memory.chat_memory.messages = message_list



    else:
        conversation_with_kg = ConversationChain(
        llm=llm, 
        verbose=True, 
        prompt=prompt,
        memory=ConversationKGMemory(llm=llm)
    )
        
        print(conversation_with_kg("where am i "))


    
    while data != "end":
        data = input()
        f = conversation_with_kg(data)
        print(f['response'])



    dd = conversation_with_kg.memory.chat_memory.json()
    with open(conversation_save_path, 'w') as file:
        json.dump(dd, file)
