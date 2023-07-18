import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak.uuids import register_uuids
import sys


UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

DATA_SERVICE_UUID = "e5700001-7bac-429a-b4ce-57ff900f479d"
DATA_RX_CHAR_UUID = "e5700002-7bac-429a-b4ce-57ff900f479d"
DATA_TX_CHAR_UUID = "e5700003-7bac-429a-b4ce-57ff900f479d"

register_uuids({
    DATA_SERVICE_UUID: "Monocle Raw Serivce",
    DATA_TX_CHAR_UUID: "Monocle Raw TX",
    DATA_RX_CHAR_UUID: "Monocle Raw RX",
})


def match_repl_uuid(device: BLEDevice, adv: AdvertisementData):
    sys.stderr.write(f"uuids={adv.service_uuids}\n")
    return UART_SERVICE_UUID.lower() in adv.service_uuids


async def get_device():
 return await BleakScanner.find_device_by_filter(match_repl_uuid)


def handle_disconnect(_: BleakClient):
    sys.stderr.write("\r\nDevice was disconnected.\r\n")
    # cancelling all tasks effectively ends the program
    for task in asyncio.all_tasks():
        task.cancel()


def handle_repl_rx(_: BleakGATTCharacteristic, data: bytearray):
    sys.stdout.write(data.decode())
    sys.stdout.flush()

async def handle_data_rx(_: BleakGATTCharacteristic, data: bytearray):
    # Here we append the received data to the audio_data variable
    global audio_data
    audio_data += data



def handle_data_rx(_: BleakGATTCharacteristic, data: bytearray):
    hex = data.hex(' ', 1)
    try:
        sys.stderr.write(f'RX: {hex} {data.decode(errors="ignore")}\r\n')
    except UnicodeDecodeError as e:
        sys.stderr.write(f"UnicodeDecodeError: {e}\r\n")
    sys.stderr.flush()
# This variable will store the output of the command
cmd_output = None

# This variable will store the output of the command
cmd_output = None

def handle_cmd_output(sender: str, data: bytearray):
    global cmd_output
    cmd_output = data

async def send_cmd_with_output(cmd: str, client: BleakClient, channel: BleakGATTCharacteristic):
    global cmd_output
    cmd_output = None  # Clear any previous output

    # Check if characteristic supports notifications
    if "notify" not in channel.properties:
        print(f"Characteristic {channel.uuid} does not support notifications")
        return

    # Start notifications on the characteristic
    await client.start_notify(channel, handle_cmd_output)

    # Send the command
    await client.write_gatt_char(channel, f"{cmd}\x04".encode())

    # Wait for the output to be received
    while cmd_output is None:
        await asyncio.sleep(0.1)

    # Stop notifications
    await client.stop_notify(channel)

    return cmd_output




async def send_cmd(cmd: str, client: BleakClient, channel: BleakGATTCharacteristic):
    await client.write_gatt_char(channel, f"{cmd}\x04".encode())
    await asyncio.sleep(1)


async def connect(device):
    async with BleakClient(device, handle_disconnect=None) as client:
        await client.start_notify(UART_TX_CHAR_UUID, handle_repl_rx)
        await client.start_notify(DATA_TX_CHAR_UUID, handle_data_rx)
        # loop = asyncio.get_running_loop()
        repl = client.services.get_service(UART_SERVICE_UUID)
        data = client.services.get_service(DATA_SERVICE_UUID)
        repl_rx_char = repl.get_characteristic(UART_RX_CHAR_UUID)
        data_rx_char = data.get_characteristic(DATA_RX_CHAR_UUID)

        # This variable will store the audio data
        audio_data = bytearray()


        await asyncio.sleep(7)
        await client.write_gatt_char(repl_rx_char, b"\x03\x01")
        await send_cmd("print('hello world')", client, repl_rx_char)
        await send_cmd("import display", client, repl_rx_char)
        await send_cmd("import bluetooth", client, repl_rx_char)
        await send_cmd("import microphone", client, repl_rx_char)
        await send_cmd("import time", client, repl_rx_char)
        await send_cmd("initial_text = display.Text('hello world', 0, 0, display.WHITE)", client, repl_rx_char)
        await send_cmd("display.show(initial_text);", client, repl_rx_char)
        await send_cmd("bluetooth.connected()", client, repl_rx_char)
        await send_cmd("len = bluetooth.max_length()", client, repl_rx_char)
        await send_cmd("str = 'world hello!'", client, repl_rx_char)
        await send_cmd("microphone.record(seconds=5.0,sample_rate=16000,bit_depth=16)", client, repl_rx_char)

        data = await send_cmd("""while True:
  chunk = microphone.read(100)
  if chunk == None:
    time.sleep(1)
    break
  bluetooth.send(chunk)
  time.sleep(0.01)
""", client, repl_rx_char)
        
        data = await send_cmd_with_output("""while True:
  chunk = microphone.read(100)
  if chunk == None:
    time.sleep(1)
    break
  bluetooth.send(chunk)
  time.sleep(0.01)
""", client, repl_rx_char)
        
        data = await send_cmd_with_output("""while True:
  chunk = microphone.read(100)
  if chunk == None:
    time.sleep(1)
    break
  bluetooth.send(chunk)
  time.sleep(0.01)
""", client, data_rx_char)
        
        # repl_rx_char.set_notify(True, handle_data_rx)
        # # After all data has been received and stored in audio_data, write it to a .wav file
        # with open('output.wav', 'wb') as f:
        #     f.write(audio_data)

        await asyncio.sleep(1)
        # await send_cmd("bluetooth.send(microphone.read(127))", client, repl_rx_char)
        response = await send_cmd("bluetooth.send(microphone.read(126))", client, repl_rx_char)
        print(response)
        
        await asyncio.sleep(3)


async def get_device_and_connect():
    device = await get_device()
    await connect(device)


# async def main():
#     async with main.MonocleAudioServer() as audio_server:
        
#         await audio_server.send_payload()
#         audio_server.process_audio()

# asyncio.run(get_device_and_connect())

if __name__ == '__main__':
    asyncio.run(get_device_and_connect())
    # asyncio.run(main())