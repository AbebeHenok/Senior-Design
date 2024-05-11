import sys
import uasyncio as asyncio
import adafruit_gps as as_GPS
from machine import UART, Pin

uart = UART(1, baudrate=9600, bits=8, stop=1, parity = None, tx=Pin(4), rx=Pin(5), timeout=300)
sreader = asyncio.StreamReader(uart)  # Create a StreamReader
gps = as_GPS.AS_GPS(sreader)  # Instantiate GPS

async def test():
    print('waiting for GPS data')
    await gps.data_received(position=True, altitude=True)

    while True:
        print('Time: {}'.format(gps.time_string()))
        print('Latitude: {}'.format((gps.latitude(1))[0]))
        print('Longitude: {}'.format((gps.longitude(1))[0]))
        print('Speed: {}'.format(gps.speed_string(11)))
        print('')
        await asyncio.sleep(5)

async def main():
    task_gps = asyncio.create_task(test())
    task_other = asyncio.create_task(concurrence_test())

    await task_gps
    await task_other

async def concurrence_test():
    while True:
        print('Testing Concurrence...')
        await asyncio.sleep(1)

asyncio.run(test())
