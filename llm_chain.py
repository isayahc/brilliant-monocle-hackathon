import asyncio
from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
import monocial_utils

def input_to_chain(ConvoChain: ConversationChain, text_input: str) -> ConversationChain:
    """
    Feed the input text into the conversation chain.

    :param ConvoChain: The conversation chain to use.
    :param text_input: The input text.
    :return: The updated conversation chain.
    """
    return ConvoChain(text_input)

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

prompt = PromptTemplate(
    input_variables=["history", "input"], 
    template=system_prompt
)

conversation_with_kg = ConversationChain(
    llm=llm, 
    verbose=True, 
    prompt=prompt,
    memory=ConversationKGMemory(llm=llm)
)
