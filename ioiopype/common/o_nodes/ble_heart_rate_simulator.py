from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
from ..utilities.realtime_clock import RealtimeClock
import threading
import time
import numpy as np

class BLEHeartRateSimulator(ODevice, RealtimeClock):
    __deviceDiscoveredEventHandler = None
    __discoveryThread = None
    __discoveryThreadRunning = False
    __devices = []

    @staticmethod
    def __discoveryThread_DoWork():
        while BLEHeartRateSimulator.__discoveryThreadRunning:
            if len(BLEHeartRateSimulator.__devices) <= 0:
                BLEHeartRateSimulator.__devices.append('HR01')
                BLEHeartRateSimulator.__devices.append('HR02')
                BLEHeartRateSimulator.__devices.append('HR03')
            if len(BLEHeartRateSimulator.__devices) > 0 and BLEHeartRateSimulator.__deviceDiscoveredEventHandler is not None:
                BLEHeartRateSimulator.__deviceDiscoveredEventHandler(BLEHeartRateSimulator.__devices)
            time.sleep(1)

    @staticmethod
    def start_scanning():
        if not BLEHeartRateSimulator.__discoveryThreadRunning:
            BLEHeartRateSimulator.__discoveryThreadRunning = True
            BLEHeartRateSimulator.__discoveryThread = threading.Thread(target=BLEHeartRateSimulator.__discoveryThread_DoWork, daemon=True)
            BLEHeartRateSimulator.__discoveryThread.start()

    @staticmethod
    def stop_scanning():
        if BLEHeartRateSimulator.__discoveryThreadRunning:
            BLEHeartRateSimulator.__discoveryThreadRunning = False
            BLEHeartRateSimulator.__discoveryThread .join()
            BLEHeartRateSimulator.__discoveryThread  = None

    @staticmethod
    def add_devices_discovered_eventhandler(handler):
        BLEHeartRateSimulator.__deviceDiscoveredEventHandler = handler

    @staticmethod
    def remove_devices_discovered_eventhandler():
        BLEHeartRateSimulator.__deviceDiscoveredEventHandler = None

    def __init__(self, name):
        super().__init__()
        self.updateRateHz = 1
        super(ONode, self).__init__(self.updateRateHz)
        self.add_o_stream(OStream(StreamInfo(0, 'HR', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'RR', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(2, 'HR1K', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(3, 'RR1K', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(2, 'BAT', StreamInfo.Datatype.Sample)))

        self.__device = None
        for device in BLEHeartRateSimulator.__devices:
            if name in device:
                self.__device = device 
        if self.__device is None:
             raise ValueError("Could find device with the entered devicename '" + name + "'.")
        
        self.__cnt = 0
        self.__t = 0
        self.__hr = [0] #1 hr value
        self.__rr = [0] #1 rr values
        self.__bat = [0] #1 bat values

        self.__hrBase = 60
        self.__hrFrequencyHz = 0.1
        self.__hrAmplitude = 5

        self.start()

    def __del__(self):
        self.stop()
        super().__del__()
        super(ONode, self).__del__()

    def update(self):    
        self.__cnt += 1
        self.__hr[0] = self.__hrBase + np.sin(2*np.pi*self.__cnt*self.__hrFrequencyHz/self.updateRateHz )*self.__hrAmplitude
        self.__rr[0] = 60000.0 / self.__hr[0]
        self.__bat = self.__cnt % 100

        #upsample to 1kHz
        rr1ktmp = None
        if self.__t > 0:
            rr1ktmp = np.array([np.linspace(self.__prevRR, self.__rr[0], num=round(self.__rr[0])+1)]).transpose()[1:,:]
        self.__t += self.__rr[0]
        self.__prevRR = self.__rr[0]

        if rr1ktmp is not None:
            rr1k = rr1ktmp
            hr1k = 60000.0 / rr1k   

            #send data
            self.write(0, np.array([self.__hr]))
            self.write(1, np.array([self.__rr]))
            self.write(2, hr1k)
            self.write(3, rr1k)
            self.write(4, np.array([self.__bat])) 