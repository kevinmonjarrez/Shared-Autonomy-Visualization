import asyncio
import json
from bleak import BleakClient
import read_json as js
import time


HUZZAH32_MAC_ADDRESS = "8C:4B:14:0E:79:A2"

SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def send_data(client, brightness, num_pixels):
    #ENCODE DATA
    data = f"{brightness},{num_pixels}".encode('utf-8')

    #WRITE DATA
    await client.write_gatt_char(CHARACTERISTIC_UUID, data)
    print(f"Data sent: {brightness}, {num_pixels}")

async def main():
    blend_data = js.blend_data
    user_data = js.user_data
    alpha_data = js.alpha_data

    async with BleakClient(HUZZAH32_MAC_ADDRESS) as client:
        connected = await client.is_connected()
        print(f"Connected: {connected}")

        while True:
            for i in range(len(user_data)-1):
                brightness = js.similarity_score(user_data[i][0], blend_data[i][0])
                num_pixels = alpha_data[i][0] / 1000
                await send_data(client, brightness, num_pixels)
                await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())
