import streamlit as st
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

def main():
    configure_environment()
    config_location = "config.json"

    if config_handler.config_exists(config_location):
        config = config_handler.load_config(config_location)

    if config is None:
        exit(1)

    conversation_save_path = config.get("conversation_save_path", "")
    llm, prompt = chat_manager.setup_conversation_chain(conversation_save_path, config)

    if Path(conversation_save_path).exists():
        conversation_with_kg = chat_manager.load_conversation(conversation_save_path, llm, prompt)
    else:
        conversation_with_kg = chat_manager.new_conversation(llm, prompt)

    st.title('My Language Model Chatbot')

    # Initialize the session state for conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Display the conversation history
    for message in st.session_state.conversation:
        sender, text = message.split(': ', 1)
        if sender == "You":
            st.markdown(f"<div style='text-align: left; color: blue;'>{sender}: {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: right; color: green;'>{sender}: {text}</div>", unsafe_allow_html=True)

    user_input = st.text_input("You: ")
    if user_input:
        st.session_state.conversation.append(f"You: {user_input}")
        bot_reply = chat_manager.interact_and_save(user_input, conversation_with_kg) # Modify this function to return the bot's response
        st.session_state.conversation.append(f"Bot: {bot_reply}")

if __name__ == '__main__':
    main()
