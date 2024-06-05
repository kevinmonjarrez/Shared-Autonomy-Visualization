import asyncio
import json
from bleak import BleakClient
import read_json as js
import time

# Huzzah32's MAC address
HUZZAH32_MAC_ADDRESS = "8C:4B:14:0E:79:A2"

SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def send_data(brightness, num_pixels):
    async with BleakClient(HUZZAH32_MAC_ADDRESS) as client:
        # Ensure we are connected
        connected = await client.is_connected()
        print(f"Connected: {connected}")

        # Prepare the data to send
        data = f"{brightness},{num_pixels}".encode('utf-8')

        # Write data to the characteristic
        await client.write_gatt_char(CHARACTERISTIC_UUID, data)
        print(f"Data sent: {brightness}, {num_pixels}")

def read_json_and_send_data(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract the numbers
    brightness = data.get("brightness", 1.0)
    num_pixels = data.get("num_pixels", 1.0)

    # Normalize the values to the expected ranges
    brightness = max(0, min(1, brightness))
    num_pixels = max(0, min(1, num_pixels))

    # Convert to appropriate ranges for the NeoPixel
    brightness = int(brightness * 255)  # Brightness from 0 to 255
    num_pixels = int(num_pixels * 8)    # Assuming 8 NeoPixels

    # Run the async function
    asyncio.run(send_data(brightness, num_pixels))

if __name__ == "__main__":
    blend_data = js.blend_data
    user_data = js.user_data
    alpha_data = js.alpha_data

    while True: 
        for i in range(len(user_data)-1):
            brightness = js.similarity_score(user_data[200][0], blend_data[200][0])
            num_pixels = alpha_data[200][0]/1000
            asyncio.run(send_data(brightness,num_pixels))
            time.sleep(0.1)
    json_file = "data.json"  # Replace with your JSON file path
    read_json_and_send_data(json_file)
