import asyncio
from bleak import BleakClient

# Use the address of your Monocle device
device_address = "CD:D3:CD:60:0F:63"

# Use the UART TX Characteristic UUID
characteristic_uuid = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

async def notification_handler(sender: int, data: bytearray):
    print(f"Received data from {sender}: {data}")

async def main():
    async with BleakClient(device_address) as client:
        await client.start_notify(characteristic_uuid, notification_handler)

        # Wait for notifications for 10 seconds
        await asyncio.sleep(60)

        await client.stop_notify(characteristic_uuid)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
