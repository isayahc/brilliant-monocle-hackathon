import asyncio
import sys

from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain

import monocle_utils
import monocle_conversation
import utils
import chat_manager

from config import configure_environment
import config_handler




async def main(model_size: str, chain: ConversationChain, save_path:str):
    try:
        async with monocle_utils.MonocleAudioServer() as audio_server:
            convo = await monocle_conversation.conversation_loop(audio_server, model_size, chain,save_path)
    except KeyboardInterrupt:
        # If the program is interrupted (e.g., by pressing Ctrl+C), save the conversation history as a .txt file.
        utils.save_conversation_as_txt(convo)

        


if __name__ == "__main__":
    # Use the function to load the configuration
    configure_environment()
    config_location = "example_config.json"

    if config_handler.config_exists(config_location):
        config = config_handler.load_config(config_location)

    if config is None:
        exit(1)

    # Use the parameters from the configuration in your script
    model_size = config.get("model_size", "medium")  # Use a default value if the key is not present
    model_name = config.get("model_name", "text-davinci-003")
    temperature = config.get("temperature", 0)
    max_tokens = config.get("max_tokens", 256)
    conversation_save_path = config.get("conversation_save_path", "conversation.json")

    configure_environment()
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


    conversation_with_kg = chat_manager.load_conversation(conversation_save_path,llm,prompt)

    

    asyncio.run(main(model_size, conversation_with_kg,save_path=conversation_save_path))
