#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ..utilities.realtime_clock import RealtimeClock
import numpy as np
import random

class DataGenerator(ONode, RealtimeClock):
    def __init__(self, sampling_rate, channel_count, signalAmplitude=10, signalFrequencyHz=1, signalOffset = 0, signalNoise = 0):
        super().__init__()
        super(ONode, self).__init__(sampling_rate)
        self.add_o_stream(OStream(StreamInfo(0, 'data', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'cnt', StreamInfo.Datatype.Frame)))
        self.sampling_rate = sampling_rate
        self.channel_count = channel_count
        self.signalAmplitude = signalAmplitude
        self.signalFrequencyHz = signalFrequencyHz
        self.signalOffset = signalOffset
        self.signalNoise = signalNoise
        self.__cnt = 0

    def __del__(self):
        super().__del__()

    def update(self):
        data = [0]*self.channel_count
        self.__cnt += 1
        for i in range(self.channel_count):
            data[i] = np.sin(2*np.pi*self.__cnt*self.signalFrequencyHz/ self.sampling_rate)*self.signalAmplitude+self.signalOffset+(random.random()-0.5)*self.signalNoise
            if i % 2 == 0:
                data[i] = data[i] * -1

        self.write(0, np.array([data]))
        self.write(1, np.array([self.__cnt]))