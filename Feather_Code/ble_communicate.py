import asyncio
from bleak import BleakClient

# Replace with your Huzzah32's MAC address
HUZZAH32_MAC_ADDRESS = "8C:4B:14:0E:79:A2"

SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def run(address):
    async with BleakClient(address) as client:
        # Ensure we are connected
        connected = await client.is_connected()
        print(f"Connected: {connected}")

        # Read the value from the characteristic
        value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print(f"Current Value: {int.from_bytes(value, byteorder='little')}")

        # Write a new value to the characteristic
        new_value = 1234
        await client.write_gatt_char(CHARACTERISTIC_UUID, new_value.to_bytes(4, byteorder='little'))
        print(f"New Value Written: {new_value}")

        # Read the value again to confirm
        value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print(f"New Value: {int.from_bytes(value, byteorder='little')}")

loop = asyncio.get_event_loop()
loop.run_until_complete(run(HUZZAH32_MAC_ADDRESS))
