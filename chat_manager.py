import json
from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory.chat_memory import ChatMemory 
from langchain.schema import ChatMessage
from pathlib import Path

from config import configure_environment
import config_handler

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
        template=system_prompt
    )
        
    return llm, prompt

def load_conversation(conversation_save_path, llm, prompt):
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

def save_conversation(conversation_with_kg, conversation_save_path):
    with open(conversation_save_path, 'w') as file:
        json.dump(conversation_with_kg.memory.chat_memory.json(), file)

def interact_and_save(conversation_with_kg, conversation_save_path):

    chat_logs = conversation_with_kg.memory.chat_memory.messages

    if not chat_logs: 
        initial_input = "where am i?"
        conversation_with_kg(initial_input)
    else:
        last_message = conversation_with_kg.memory.chat_memory.messages[-1].text
        print(last_message)

    user_input = input()
    while user_input != "end":
        response = conversation_with_kg(user_input)
        print(response['response'])
        user_input = input()

    save_conversation(conversation_with_kg, conversation_save_path)



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

