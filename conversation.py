# conversation.py

from langchain.chains import ConversationChain
from langchain.schema import ChatMessage
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory import chat_memory


import utils
import monocle_utils
import chat_manager

import json



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
    return chat_manager.input_to_chain(conversation_with_kg, transcribed_text)


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
        response_chain = chat_manager.input_to_chain(conversation_with_kg, initial_text)
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

        chat_manager.save_conversation(conversation_with_kg)

        return convo


 