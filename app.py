import asyncio
from bleak import BleakScanner
import time

TARGET_MAC = "XX:XX:XX:XX:XX:XX"  # your phone's BLE MAC
COOLDOWN_SECONDS = 60
last_trigger_time = 0


async def scan():
    global last_trigger_time

    while True:
        devices = await BleakScanner.discover(timeout=5.0)

        for d in devices:
            if d.address == TARGET_MAC:
                now = time.time()

                if now - last_trigger_time > COOLDOWN_SECONDS:
                    print("Recognized device nearby!")
                    trigger_transfer()
                    last_trigger_time = now
                else:
                    print("Device seen but in cooldown")

        await asyncio.sleep(2)

def trigger_transfer():
    print("Triggering transfer logic...")
    # TODO: call your backend API here

asyncio.run(scan())