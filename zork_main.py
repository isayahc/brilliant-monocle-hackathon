from langchain.chains.conversation.memory import ConversationBufferMemory
# from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

# from langchain.memory import StreamlitChatMessageHistory

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

import streamlit as st

import openai
import os

OPEN_AI_KEY = "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"
openai.api_key = OPEN_AI_KEY
# history = StreamlitChatMessageHistory(key="chat_messages")

# Optionally, specify your own session_state key for storing messages
# msgs = StreamlitChatMessageHistory(key="special_app_key")

# memory = ConversationBufferMemory(memory_key="history", chat_memory=msgs)



# template = """You are an AI chatbot having a conversation with a human.

# {history}
# Human: {human_input}
# AI: """

# template = """
# You are a game master for a Zork-style game. You must keep track of the user's game states, 
# and provide a fun and challenging experience. Zork is a classic text-based adventure game, 
# assist in generating text-based responses and managing the game's logic.

# {history}

# Conversation:
# Human: {input}
# AI:
# """

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
# template = """You are an AI chatbot having a conversation with a human.

# {history}
# Human: {human_input}
# AI: """
# prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

# Add the memory to an LLMChain as usual
# llm_chain = LLMChain(llm=OpenAI(), prompt=prompt, memory=memory)

template = """
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
    template=template
)

# prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

# Add the memory to an LLMChain as usual
# history = StreamlitChatMessageHistory(key="chat_messages")
# memory = ConversationBufferMemory(memory_key="history", chat_memory=msgs)

# msgs = StreamlitChatMessageHistory(key="special_app_key")

memory = ConversationBufferMemory(memory_key="history", )

llm_chain = LLMChain(llm=OpenAI(), prompt=prompt, memory=memory)

msgs = memory.chat_memory

# if len(msgs.messages) == 0:
#     # msgs.add_ai_message("How can I help you?")
#     text= "How can I help you?"
#     llm_chain(text)



# for msg in msgs.messages:
#     st.chat_message(msg.type).write(msg.content)

# if prompt := st.chat_input():
#     st.chat_message("human").write(prompt)

#     # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
#     response = llm_chain.run(prompt)
#     st.chat_message("ai").write(response)


for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
    response = llm_chain.run(prompt)
    st.chat_message("ai").write(response)