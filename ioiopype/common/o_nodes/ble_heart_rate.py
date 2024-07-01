import asyncio
import threading
from bleak import *
from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
import numpy as np
import time

class BLEHeartRate(ODevice):
    HR_SERVICE_UUID = '0000180d-0000-1000-8000-00805f9b34fb'
    HR_NOTIFY_CHARACTERISTIC_UUID = '00002a37-0000-1000-8000-00805f9b34fb'
    RR_CONVERSION_FACTOR = (1000.0/1024.0)

    __eventHandler = None
    __scanner = None
    __loop = None
    __thread = None
    __devices : BLEDevice = []
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
        if BLEHeartRate.HR_SERVICE_UUID in advertisement_data.service_uuids:
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
        self.add_o_stream(OStream(StreamInfo(2, 'HR1K', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(3, 'RR1K', StreamInfo.Datatype.Sample)))

        self.__t = 0
        self.__prevRR = 0

        if not BLEHeartRate.__devices:
            BLEHeartRate.start_scanning()
            start = time.time()
            while name not in  BLEHeartRate.__deviceNames and end - start <= 5:      
                asyncio.sleep(0.1)
                end = time.time()
            if end - start > 5:
                raise ValueError('Could not find ' + name + 'within defined time interval.')

        BLEHeartRate.stop_scanning()
        if not BLEHeartRate.__devices or not BLEHeartRate.__deviceNames:
            raise ValueError('No BLE heart rate devices discovered.')

        self.__device=None
        for device in BLEHeartRate.__devices:
            if device.name == name:
                self.__device = device
                break
        
        if self.__device is None:
            raise ValueError('Could not find device with the defined device name')
        
        asyncio.run_coroutine_threadsafe(self.__open(), BLEHeartRate.__loop)

    async def __open(self):
        self.__client = BleakClient(self.__device)
        await self.__client.connect()
        hrCharacteristic = None
        if self.__client.is_connected:
            services = self.__client.services
            for service in services:
                characteristics = service.characteristics
                for characteristic in characteristics:
                    if characteristic.uuid == BLEHeartRate.HR_NOTIFY_CHARACTERISTIC_UUID:
                        hrCharacteristic = characteristic
                        break
                if hrCharacteristic is not None: 
                    break
            if hrCharacteristic is None:
                raise ValueError('Could not find hr notify characteristic')
        
            await self.__client .start_notify(hrCharacteristic, self.__hrNotify)
        else:
            raise ValueError('Connection failed')

    async def __close(self):
        await self.__client.disconnect()
        print('disconnected')

    def __hrNotify(self, characteristic: BleakGATTCharacteristic, data: bytearray):
        formatUint8 = True
        rrAvailable = True
        if (data[0] & 0x01) == 0:
            formatUint8 = True
        else:
            formatUint8 = False

        # Check the fifth bit to determine rrAvailable
        if (data[0] & 0x10) == 0x10:
            rrAvailable = True
        else:
            rrAvailable = False
        
        # Get heart rate
        hr = 0.0
        if formatUint8:
            hr = data[1]
        else:
            hr = float((data[2] << 8) | data[1])
        
        # Get RR intervals
        dataSize = len(data) 
        rrValues = []
        numberOfRRIntervalsReceived = 0
        if rrAvailable:
            if formatUint8:
                offset = 2
            else:
                offset = 3

            rrIntervalsBinaryLength = dataSize - offset
            if rrIntervalsBinaryLength > 0:
                rrIntervalsBinary = data[offset:offset + rrIntervalsBinaryLength]
                numberOfRRIntervalsReceived = rrIntervalsBinaryLength // 2
                
                for i in range(0, rrIntervalsBinaryLength, 2):
                    rr_value = float((rrIntervalsBinary[i + 1] << 8) | rrIntervalsBinary[i]) * BLEHeartRate.RR_CONVERSION_FACTOR
                    rrValues.append(rr_value)
        else:
            numberOfRRIntervalsReceived = 1
            rrValues.append(60000.0 / hr)

        #upsample to 1kHz
        rr1ktmp = []
        for rrValue in rrValues:
            if self.__t <= 0 and self.__prevRR <= 0:
                rr1ktmp.append(np.array([[rrValue]]))
            else:
                rr1ktmp.append(np.array([np.linspace(self.__prevRR, rrValue, num=round(rrValue))+1]).transpose()[1:,:])
            self.__t += rrValue
            self.__prevRR = rrValue    
        if len(rr1ktmp) > 1:
            rr1k = np.concatenate(rr1ktmp, axis=0)
        else:
            rr1k = rr1ktmp[0]
        hr1k = 60000.0 / rr1k   
        
        #send data
        self.write(0, hr) 
        for rrValue in rrValues:
            self.write(1, rrValue) 
        self.write(2, hr1k) 
        self.write(3, rr1k)

    def __del__(self):
        super().__del__()
        asyncio.run_coroutine_threadsafe(self.__close(), BLEHeartRate.__loop)