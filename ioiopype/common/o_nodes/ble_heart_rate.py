import asyncio
import threading
from bleak import *
from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
import time

class BLEHeartRate(ODevice):
    HR_UUID = '0000180d-0000-1000-8000-00805f9b34fb'

    __eventHandler = None
    __scanner = None
    __loop = None
    __thread = None
    __devices = []
    __deviceNames = []

    def __initializeLoop():
        if BLEHeartRate.__loop is None:
            BLEHeartRate.__loop = asyncio.new_event_loop()
            BLEHeartRate.__thread = threading.Thread(target=BLEHeartRate.__runLoop, daemon=True)
            BLEHeartRate.__thread.start()

    def __runLoop():
        BLEHeartRate.__loop.run_forever()

    @staticmethod
    def __device_discovered_callback(device : BLEDevice, advertisement_data : AdvertisementData): 
        if BLEHeartRate.HR_UUID in advertisement_data.service_uuids:
            if device not in BLEHeartRate.__devices:
                BLEHeartRate.__devices.append(device)
                BLEHeartRate.__deviceNames.append(device.name)
                if BLEHeartRate.__eventHandler is not None:
                    BLEHeartRate.__eventHandler(BLEHeartRate.__deviceNames)

    @staticmethod
    async def __start_scanning():
        if  BLEHeartRate.__scanner is None:
            BLEHeartRate.__scanner = BleakScanner(detection_callback=BLEHeartRate.__device_discovered_callback, cb=dict(use_bdaddr=False))
        await BLEHeartRate.__scanner.start()

    @staticmethod
    async def __stop_scanning():
        if  BLEHeartRate.__scanner is not None:
            await BLEHeartRate.__scanner.stop()
        BLEHeartRate.__scanner = None

    @staticmethod
    def start_scanning():
        BLEHeartRate.__initializeLoop()
        asyncio.run_coroutine_threadsafe(BLEHeartRate.__start_scanning(), BLEHeartRate.__loop)

    @staticmethod
    def stop_scanning():
        BLEHeartRate.__initializeLoop()
        asyncio.run_coroutine_threadsafe(BLEHeartRate.__stop_scanning(), BLEHeartRate.__loop)

    @staticmethod
    def add_devices_discovered_eventhandler(handler):
        BLEHeartRate.__initializeLoop()
        BLEHeartRate.__eventHandler = handler

    @staticmethod
    def remove_devices_discovered_eventhandler():
        BLEHeartRate.__initializeLoop()
        BLEHeartRate.__eventHandler = None

    def __init__(self, name):
        super().__init__()
        self.add_o_stream(OStream(StreamInfo(0, 'HR', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'RR', StreamInfo.Datatype.Sample)))

    def __del__(self):
        super().__del__()