import asyncio
import monocial_utils

async def main():
    async with monocial_utils.MonocleAudioServer() as audio_server:
        data = await audio_server.send_audio_data()
        # data = await monocial_utils.send_audio_data()
        # convo = await conversation_loop(audio_server, model_size)

if __name__ == '__main__':
    asyncio.run(main())