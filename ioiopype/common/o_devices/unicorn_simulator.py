from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
from ..utilities.realtime_clock import RealtimeClock
import threading
import time
import numpy as np
import random
import math

class UnicornSimulator(ODevice, RealtimeClock):
    NumberOfAcquiredChannels = 17
    SamplingRateInHz = 250
    NumberOfEEGChannels = 8
    NumberOfAccChannels = 3
    NumberOfGyrChannels = 3
    NumberOfCntChannels = 1
    NumberOfBatChannels = 1
    NumberOfValidChannels = 1

    __deviceDiscoveredEventHandler = None
    __discoveryThread = None
    __discoveryThreadRunning = False
    
    @staticmethod
    def get_available_devices():
        devices = []
        devices.append('UN-0000.00.00')
        devices.append('UN-0000.00.01')
        devices.append('UN-0000.00.02')
        return devices

    @staticmethod
    def __discoveryThread_DoWork():
        while UnicornSimulator.__discoveryThreadRunning:
            serials = UnicornSimulator.get_available_devices()
            if len(serials) > 0 and UnicornSimulator.__deviceDiscoveredEventHandler is not None:
                UnicornSimulator.__deviceDiscoveredEventHandler(serials)
            time.sleep(1)

    @staticmethod
    def start_scanning():
        if not UnicornSimulator.__discoveryThreadRunning:
            UnicornSimulator.__discoveryThreadRunning = True
            UnicornSimulator.__discoveryThread = threading.Thread(target=UnicornSimulator.__discoveryThread_DoWork, daemon=True)
            UnicornSimulator.__discoveryThread.start()

    @staticmethod
    def stop_scanning():
        if UnicornSimulator.__discoveryThreadRunning:
            UnicornSimulator.__discoveryThreadRunning = False
            UnicornSimulator.__discoveryThread .join()
            UnicornSimulator.__discoveryThread  = None

    @staticmethod
    def add_devices_discovered_eventhandler(handler):
        UnicornSimulator.__deviceDiscoveredEventHandler = handler

    @staticmethod
    def remove_devices_discovered_eventhandler():
        UnicornSimulator.__deviceDiscoveredEventHandler = None

    def __init__(self, serial):
        super().__init__()
        super(ONode, self).__init__(UnicornSimulator.SamplingRateInHz)
        self.add_o_stream(OStream(StreamInfo(0, 'EEG', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'ACC', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(2, 'GYR', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(3, 'CNT', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(4, 'BAT', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(5, 'VALID', StreamInfo.Datatype.Sample)))

        self.__devices = UnicornSimulator.get_available_devices()
        self.__device = None
        for device in self.__devices:
            if serial in device:
                self.__device = device 
        if self.__device is None:
             raise ValueError("Could find device with the specified serial number '" + serial + "'.")
        
        self.__eeg = [0]*UnicornSimulator.NumberOfEEGChannels
        self.__acc = [0]*UnicornSimulator.NumberOfAccChannels
        self.__gyr = [0]*UnicornSimulator.NumberOfGyrChannels
        self.__cnt = [0]*UnicornSimulator.NumberOfCntChannels
        self.__bat = [0]*UnicornSimulator.NumberOfBatChannels
        self.__valid = [0]*UnicornSimulator.NumberOfValidChannels

        self.__eegSignalFrequencyHz = 10
        self.__eegSignalAmplitudeuV = 20
        self.__eegSignalOffsetuV = 20000
        self.__eegPowerLineFrequencyHz = 50
        self.__eegPowerLineAmplitude = 1000
        self.__eegSignalNoise = 5

        self.start()

    def __del__(self):
        self.stop()
        super().__del__()
        super(ONode, self).__del__()

    def __send_data(self):
        self.write(0, np.array([self.__eeg])) 
        self.write(1, np.array([self.__acc])) 
        self.write(2, np.array([self.__gyr])) 
        self.write(3, np.array([self.__cnt])) 
        self.write(4, np.array([self.__bat]))  
        self.write(5, np.array([self.__valid])) 

    def __generate_data(self):
        self.__cnt[0] += 1
        for i in range(len(self.__eeg)):
            self.__eeg[i] = (np.sin(2*np.pi*self.__cnt[0]*self.__eegSignalFrequencyHz/ UnicornSimulator.SamplingRateInHz)*self.__eegSignalAmplitudeuV +
                             np.sin(2*np.pi*self.__cnt[0]*self.__eegPowerLineFrequencyHz/ UnicornSimulator.SamplingRateInHz)*self.__eegPowerLineAmplitude +
                             self.__eegSignalOffsetuV + 
                             (random.random()-0.5)*self.__eegSignalNoise)
            if i % 2 == 0:
                self.__eeg[i]  = self.__eeg[i]  * -1

        for i in range(len(self.__acc)):
            if i == 0:
                self.__acc[i] = (np.sin(2*np.pi*self.__cnt[0]/ UnicornSimulator.SamplingRateInHz)) / math.sqrt(2)
            if i == 1:
                self.__acc[i] = (np.cos(2*np.pi*self.__cnt[0]/ UnicornSimulator.SamplingRateInHz)) / math.sqrt(2)
            if i == 2:
                self.__acc[i] = (np.sin(2*np.pi*self.__cnt[0]/ UnicornSimulator.SamplingRateInHz)) * -1 / math.sqrt(2)
        
        for i in range(len(self.__gyr)):
            if i == 0:
                self.__gyr[i] = (np.sin(2*np.pi*self.__cnt[0]/ UnicornSimulator.SamplingRateInHz)) / math.sqrt(2)
            if i == 1:
                self.__gyr[i] = (np.cos(2*np.pi*self.__cnt[0]/ UnicornSimulator.SamplingRateInHz)) / math.sqrt(2)
            if i == 2:
                self.__gyr[i] = (np.sin(2*np.pi*self.__cnt[0]/ UnicornSimulator.SamplingRateInHz)) * -1 / math.sqrt(2)

        self.__bat[0] = self.__cnt[0] % 100
        if self.__cnt[0] % UnicornSimulator.SamplingRateInHz:
            self.__valid[0] = 0
        else:
            self.__valid[0] = 1

    def update(self):    
        self.__generate_data()
        self.__send_data()
