import asyncio
import threading
from bleak import *
from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
import time

class BLEHeartRate(ODevice):
    __bleakScanner = None
    __loop = None
    __deviceDiscoveredEventHandler = None

    @staticmethod
    def __initialize_loop():
        if BLEHeartRate.__loop is None:
            def bleak_thread():
                asyncio.set_event_loop(BLEHeartRate.__loop)
                if not BLEHeartRate.__loop.is_running():
                    BLEHeartRate.__loop.run_forever()
            BLEHeartRate.__loop = asyncio.new_event_loop()
            t = threading.Thread(target=bleak_thread)
            t.start()

    @staticmethod
    def __uninitialize_loop():
        if BLEHeartRate.__loop is not None:
            BLEHeartRate.__loop.call_soon_threadsafe(BLEHeartRate.__loop.stop)

    @staticmethod
    async def __initialize_bleak():
        if BLEHeartRate.__bleakScanner is None:
            BLEHeartRate.__bleakScanner = BleakScanner(BLEHeartRate.__deviceDiscoveredCallback, scanning_mode='active', cb=dict(use_bdaddr=False))
    
    @staticmethod
    async def __uninitialize_bleak():
        if BLEHeartRate.__bleakScanner is not None:
            BLEHeartRate.__bleakScanner = None

    @staticmethod
    def __deviceDiscoveredCallback(device: BLEDevice, advertisement_data: AdvertisementData):
        print("%s: %r", device.address, advertisement_data)

    @staticmethod
    async def __startScanning():
        await BLEHeartRate.__initialize_bleak()
        await BLEHeartRate.__bleakScanner.start()

    @staticmethod
    async def __stopScanning():
        await BLEHeartRate.__bleakScanner.stop()

    @staticmethod
    def start_scanning():
        BLEHeartRate.__initialize_loop()
        BLEHeartRate.__loop.run_until_complete(BLEHeartRate.__initialize_bleak())
        BLEHeartRate.__loop.run_until_complete(BLEHeartRate.__startScanning())

    @staticmethod
    def stop_scanning():
        BLEHeartRate.__loop.run_until_complete(BLEHeartRate.__stopScanning())

    @staticmethod
    def add_devices_discovered_eventhandler(handler):
        BLEHeartRate.__initialize_loop()
        BLEHeartRate.__loop.run_until_complete(BLEHeartRate.__initialize_bleak())
        BLEHeartRate.__deviceDiscoveredEventHandler = handler

    @staticmethod
    def remove_devices_discovered_eventhandler():
        BLEHeartRate.__deviceDiscoveredEventHandler = None
    
    def __init__(self, name):
        super().__init__()
        self.add_o_stream(OStream(StreamInfo(0, 'HR', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'RR', StreamInfo.Datatype.Sample)))

    def __del__(self):
        super().__del__()