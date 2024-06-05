import asyncio
from bleak import BleakScanner

async def run():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Found device: {device.name}, Address: {device.address}")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
