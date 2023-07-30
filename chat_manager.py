import json
from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory.chat_memory import ChatMemory 
from langchain.schema import ChatMessage
from pathlib import Path

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
        #if there is no chat history start from the begining
        initial_input = "where am i?"
        conversation_with_kg(initial_input)
    else:
        #if there is a chat history start from there
        last_message = conversation_with_kg.memory.chat_memory.messages[-1].text
        print(last_message)

    user_input = input()
    while user_input != "end":
        response = conversation_with_kg(user_input)
        print(response['response'])
        user_input = input()


    with open(conversation_save_path, 'w') as file:
        json.dump(conversation_with_kg.memory.chat_memory.json(), file)