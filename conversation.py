# conversation.py

from langchain.chains import ConversationChain
from langchain.schema import ChatMessage
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory import chat_memory


import utils
import monocle_utils


import json


def input_to_chain(
        conversation_chain: ConversationChain, 
        text_input: str
        ) -> ConversationChain:
    """
    Feed the input text into the conversation chain.

    :param conversation_chain: The conversation chain to use.
    :type conversation_chain: ConversationChain
    :param text_input: The input text to be processed by the conversation chain.
    :type text_input: str
    :return: The updated conversation chain after processing the input text.
    :rtype: ConversationChain
    """
    return conversation_chain(text_input)


# def generate_and_play_response(conversation_with_kg:ConversationChain, text:str) -> dict:
#     """
#     Generate a response using the conversation chain and play it as speech.

#     :param conversation_with_kg: The conversation chain to use.
#     :type conversation_with_kg: ConversationChain
#     :param text: The input text to be processed by the conversation chain.
#     :type text: str
#     :return: The response generated by the conversation chain.
#     :rtype: dict
#     """
#     response = input_to_chain(conversation_with_kg, text)
#     utils.generate_and_play_speech(response['response'])
#     return response

# def generate_and_play_response(conversation_with_kg:ConversationChain, text:str) -> None:
#     """
#     Generate a response using the conversation chain and play it as speech.

#     :param conversation_with_kg: The conversation chain to use.
#     :type conversation_with_kg: ConversationChain
#     :param text: The input text to be processed by the conversation chain.
#     :type text: str
#     :return: The response generated by the conversation chain.
#     :rtype: dict
#     """
#     response = input_to_chain(conversation_with_kg, text)
#     utils.generate_and_play_speech(response['response'])
    # return response

async def handle_conversation_turn(
        audio_server:monocle_utils.MonocleAudioServer, 
        model_size:str, 
        conversation_with_kg:ConversationChain
        ) -> ConversationChain:
    """
    Handle a single turn of the conversation by receiving audio input, transcribing it, generating a response,
    and playing the response as speech.

    :param audio_server: The MonocleAudioServer to receive audio input.
    :type audio_server: monocle_utils.MonocleAudioServer
    :param model_size: The size of the model used for transcription.
    :type model_size: str
    :param conversation_with_kg: The conversation chain to use.
    :type conversation_with_kg: ConversationChain
    :return: The response generated by the conversation chain.
    :rtype: dict
    """
    await audio_server.send_payload()
    audio_server.write_audio()
    transcribed_text = utils.transcribe(monocle_utils.AUDIO_OUTPUT_PATH, model_size)
    # return  generate_and_play_response(conversation_with_kg, transcribed_text)
    return input_to_chain(conversation_with_kg, transcribed_text)


async def conversation_loop(
        audio_server: monocle_utils.MonocleAudioServer, 
        model_size: str, 
        conversation_with_kg: ConversationChain
        ) -> list:
    """
    Run the conversation loop, where the conversation chain interacts with the user in a back-and-forth manner.

    :param audio_server: The MonocleAudioServer to receive audio input.
    :type audio_server: monocle_utils.MonocleAudioServer
    :param model_size: The size of the model used for transcription.
    :type model_size: str
    :param conversation_with_kg: The conversation chain to use.
    :type conversation_with_kg: ConversationChain
    :return: A list containing the history of the conversation as a sequence of responses.
    :rtype: List[dict]
    """
    convo = []
    try:
        initial_text = "Where am I"
        # response = generate_and_play_response(conversation_with_kg, initial_text)
        response_chain = input_to_chain(conversation_with_kg, initial_text)
        response_text = response_chain['response']
        convo.append(response_text)
        while response_chain['input'] != "end game":
            response = await handle_conversation_turn(audio_server, model_size, conversation_with_kg)
            convo.append(response)
    except KeyboardInterrupt:
        # If the conversation loop is interrupted, return the conversation history
        print("\nConversation loop interrupted.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:

        save_conversation(conversation_with_kg)

        return convo

def extract_langchain_messages(conversation_with_kg: ConversationChain) -> list[ChatMessage]:
    return conversation_with_kg.chat_memory.messages

def save_conversation(conversation_with_kg: ConversationChain) -> str:
    return conversation_with_kg.json()

def load_conversation(conversation_json: str,llm) -> ConversationChain:
    conversation_json =  json.load(conversation_json)
    retrieved_memory = ConversationBufferMemory(chat_memory=conversation_json)

    reloaded_chain = ConversationChain(
    llm=llm,
    verbose=True,
    memory=retrieved_memory,
    chat_memory=chat_memory
    )

    return reloaded_chain
 