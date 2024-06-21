import asyncio
import threading
from bleak import *

class BLEScanner():
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.__runLoop, daemon=True)
        self.thread.start()

    def __del__(self):
        self.loop.stop()

    def __device_discovered_callback(self, device, advertisement_data):
        print("%s: %r", device.address, advertisement_data)

    def __runLoop(self):
        self.loop.run_forever()

    async def __start_scanning(self):
        self.scanner = BleakScanner(detection_callback=self.__device_discovered_callback, cb=dict(use_bdaddr=False))
        await self.scanner.start()

    async def __stop_scanning(self):
        await self.scanner.stop()
        self.scanner = None

    def start_scanning(self):
        asyncio.run_coroutine_threadsafe(self.__start_scanning(), self.loop)

    def stop_scanning(self):
        asyncio.run_coroutine_threadsafe(self.__stop_scanning(), self.loop)

def __main__():
    s = BLEScanner()
    s.start_scanning()
    input('Press ENTER to terminate the application')
    s.stop_scanning()
    del s

__main__()