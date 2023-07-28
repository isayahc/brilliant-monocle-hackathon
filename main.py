import asyncio

from langchain.chains.conversation.memory import ConversationKGMemory
from langchain import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain

import monocle_utils
import conversation


async def main(model_size:str,chain:ConversationChain):

    async with monocle_utils.MonocleAudioServer() as audio_server:

        convo = await conversation.conversation_loop(audio_server,model_size,chain)

if __name__ == "__main__":
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

    model_size = "medium"
    asyncio.run(main(model_size,conversation_with_kg))
