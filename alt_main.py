import asyncio
import json
import sys

from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory.chat_memory import ChatMemory 
from langchain.schema import ChatMessage

import monocle_utils
import monocle_conversation
import utils
import chat_manager
import config_handler

from config import configure_environment
from pathlib import Path

import streamlit as st

import openai



if __name__ == "__main__":
    configure_environment()
    config_location = "config.json"

    if config_handler.config_exists(config_location):
        config = config_handler.load_config(config_location)

    

    if config is None:
        exit(1)

    conversation_save_path = config.get("conversation_save_path", "")

    llm, prompt = chat_manager.setup_conversation_chain(conversation_save_path, config)

    OPENAI_API_KEY = ""
    
    if Path(conversation_save_path).exists():
        conversation_with_kg = chat_manager.load_conversation(conversation_save_path, llm, prompt)
    else:
        conversation_with_kg = chat_manager.new_conversation(llm, prompt)

    OPEN_AI_KEY: str = st.text_input("Enter API key", type="password")
    if OPEN_AI_KEY:
        # st.write(f"API Key: {OPEN_AI_KEY}")
        openai.api_key = OPEN_AI_KEY

    for msg in conversation_with_kg.memory.chat_memory.messages:
        st.chat_message(msg.type).write(msg.content['reponse'])

    if prompt := st.chat_input():
        st.chat_message("human").write(prompt)

        # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
        response = conversation_with_kg(prompt)['response']
        
        st.chat_message("ai").write(response)


    # chat_manager.interact_and_save(conversation_with_kg, conversation_save_path)

