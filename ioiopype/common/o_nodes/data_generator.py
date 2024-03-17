#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ..utilities.realtime_clock import RealtimeClock
import numpy as np
import random
import json

class DataGenerator(ONode, RealtimeClock):
    def __init__(self, samplingRate, channelCount, signalAmplitude=10, signalFrequencyHz=1, signalOffset = 0, signalNoise = 0):
        super().__init__()
        super(ONode, self).__init__(samplingRate)
        self.add_o_stream(OStream(StreamInfo(0, 'data', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'cnt', StreamInfo.Datatype.Sample)))
        self.samplingRate = samplingRate
        self.channelCount = channelCount
        self.signalAmplitude = signalAmplitude
        self.signalFrequencyHz = signalFrequencyHz
        self.signalOffset = signalOffset
        self.signalNoise = signalNoise
        self.__cnt = 0

    def __del__(self):
        super().__del__()
        super(ONode, self).__del__()

    def __dict__(self):
        ostreams = []
        for i in range(0,len(self.OutputStreams)):
            ostreams.append(self.OutputStreams[i].StreamInfo.__dict__())
        return {
            "name": self.__class__.__name__,
            "samplingRate": self.samplingRate,
            "channelCount": self.channelCount,
            "signalAmplitude": self.signalAmplitude,
            "signalFrequencyHz": self.signalFrequencyHz,
            "signalOffset": self.signalOffset,
            "signalNoise": self.signalNoise,
            "o_streams": ostreams
        }
    
    def __str__(self):
        return json.dumps(self.__dict__(), indent=4)

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)

    def update(self):
        data = [0]*self.channelCount
        self.__cnt += 1
        for i in range(self.channelCount):
            data[i] = np.sin(2*np.pi*self.__cnt*self.signalFrequencyHz/ self.samplingRate)*self.signalAmplitude+self.signalOffset+(random.random()-0.5)*self.signalNoise
            if i % 2 == 0:
                data[i] = data[i] * -1

        self.write(0, np.array([data]))
        self.write(1, np.array([self.__cnt]))