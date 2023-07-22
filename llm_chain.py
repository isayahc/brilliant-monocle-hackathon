
from langchain.chains import ConversationChain


def input_to_chain(ConvoChain: ConversationChain, text_input: str) -> ConversationChain:
    """
    Feed the input text into the conversation chain.

    :param ConvoChain: The conversation chain to use.
    :param text_input: The input text.
    :return: The updated conversation chain.
    """
    return ConvoChain(text_input)

