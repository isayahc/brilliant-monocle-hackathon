import asyncio
# from mic import get_device
import mic

# async def get_device_and_connect():
#     device = await get_device()
#     await connect(device)

if __name__ == "__main__":
    # asyncio.run(main())
    # asyncio.run(mic.get_device())
    mic.register_uuids()
    asyncio.run(mic.get_device_and_connect())