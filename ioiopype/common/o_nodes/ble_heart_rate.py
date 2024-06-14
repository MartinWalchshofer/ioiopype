import asyncio
from bleak import *
from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice

class BLEHeartRate(ODevice):
    __bleakScanner = None

    @staticmethod
    def __deviceDiscoveredCallback(device: BLEDevice, advertisement_data: AdvertisementData):
        print("%s: %r", device.address, advertisement_data)

    @staticmethod
    def __initialize():
       if BLEHeartRate.__bleakScanner is None:
            scanner = BleakScanner(BLEHeartRate.__deviceDiscoveredCallback)
    
    @staticmethod
    def __uninitialize():
       if BLEHeartRate.__bleakScanner is not None:
            BLEHeartRate.__bleakScanner = None

    @staticmethod
    def start_scanning():
        BLEHeartRate.__initialize()
        BLEHeartRate.__bleakScanner.start()

    @staticmethod
    def stop_scanning():
        BLEHeartRate.__bleakScanner.stop()
        BLEHeartRate.__uninitialize()

    @staticmethod
    def add_devices_discovered_eventhandler(handler):
        BLEHeartRate.__initialize()

    @staticmethod
    def remove_devices_discovered_eventhandler():
        pass
    
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