import asyncio
from bleak import *
from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice

class BLEHeartRate(ODevice):
    __bleakScanner = None
    __loop = None

    @staticmethod
    def __runAsync(function):
        if BLEHeartRate.__loop is None:
            BLEHeartRate.__loop = asyncio.new_event_loop()
            asyncio.set_event_loop(BLEHeartRate.__loop)
        return BLEHeartRate.__loop.run_until_complete(function)

    @staticmethod
    def __deviceDiscoveredCallback(device: BLEDevice, advertisement_data: AdvertisementData):
        print("%s: %r", device.address, advertisement_data)

    @staticmethod
    async def __initialize():
       if BLEHeartRate.__bleakScanner is None:
            BLEHeartRate.__bleakScanner = BleakScanner(BLEHeartRate.__deviceDiscoveredCallback)
    
    @staticmethod
    async def __uninitialize():
       if BLEHeartRate.__bleakScanner is not None:
            BLEHeartRate.__bleakScanner = None

    @staticmethod
    async def __startScanning():
        if BLEHeartRate.__bleakScanner is None:
            BLEHeartRate.__bleakScanner = BleakScanner(BLEHeartRate.__deviceDiscoveredCallback)
        await BLEHeartRate.__bleakScanner.start()

    @staticmethod
    async def __stopScanning():
        await BLEHeartRate.__bleakScanner.stop()

    @staticmethod
    def start_scanning():
        BLEHeartRate.__runAsync(BLEHeartRate.__initialize())
        BLEHeartRate.__runAsync(BLEHeartRate.__startScanning())

    @staticmethod
    def stop_scanning():
        BLEHeartRate.__runAsync(BLEHeartRate.__stopScanning())

    @staticmethod
    def add_devices_discovered_eventhandler(handler):
        BLEHeartRate.__runAsync(BLEHeartRate.__initialize())
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

'''async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

def test():
    asyncio.run(main())

test()'''