import alt_server

import asyncio
from bleak import BleakScanner, BleakClient

async def scan_bluetooth_devices():
    devices = await BleakScanner.discover()
    devices_list = []
    for device in devices:
        devices_list.append({"name": device.name, "address": device.address})
    return devices_list

async def get_services(mac_addr: str):
    services = []
    try:
        async with BleakClient(mac_addr) as client:
            svcs = await client.get_services()
            for service in svcs:
                services.append({"device": mac_addr, "service": service.uuid})
    except Exception as e:
        print(f"An error occurred while trying to connect to the device {mac_addr} or retrieve its services: {e}")
    return services



devices = asyncio.run(scan_bluetooth_devices())
devices = ["CD:D3:CD:60:0F:63", "6D:A5:92:C8:2C:88", "00:B8:DB:FA:7B:4A", "4A:7D:E6:9A:BA:A3", "09:74:9B:A1:A6:E5", "5B:B9:87:89:3B:A0"]

all_services = []
for device in devices:
    device_services = asyncio.run(get_services(device))
    all_services.extend(device_services)

x = 0