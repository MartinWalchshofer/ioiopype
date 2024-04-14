#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ..utilities.realtime_clock import RealtimeClock
import numpy as np
import json
from enum import Enum

class SignalGenerator(ONode, RealtimeClock):
    class SignalMode(Enum):
        Sine = 1
        Square = 2
        Sawtooth = 3
        Triangle = 4

    def __init__(self, samplingRate, channelCount, mode, signalAmplitude=10, signalFrequencyHz=1, signalOffset = 0):
        super().__init__()
        super(ONode, self).__init__(samplingRate)
        self.add_o_stream(OStream(StreamInfo(0, 'data', StreamInfo.Datatype.Sample)))
        self.samplingRate = samplingRate
        self.channelCount = channelCount
        self.signalAmplitude = signalAmplitude
        self.signalFrequencyHz = signalFrequencyHz
        self.signalOffset = signalOffset
        self.mode = mode
        self.__cnt = 0
        self.__periodSamples = samplingRate * 1/signalFrequencyHz
        self.__halfPeriodSamples = samplingRate * 1/(signalFrequencyHz*2)
        if self.mode == SignalGenerator.SignalMode.Square:
            self.__direction = 1
        if self.mode == SignalGenerator.SignalMode.Sawtooth:
            self.__k = signalAmplitude * 2 / self.__periodSamples
        if self.mode == SignalGenerator.SignalMode.Triangle:
            self.__direction = 1
            self.__k = signalAmplitude * 2 / self.__halfPeriodSamples
            

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
            "mode": self.mode.name,
            "signalAmplitude": self.signalAmplitude,
            "signalFrequencyHz": self.signalFrequencyHz,
            "signalOffset": self.signalOffset,
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
        if self.mode == SignalGenerator.SignalMode.Sine:
            for i in range(self.channelCount):
                data[i] = np.sin(2*np.pi*self.__cnt*self.signalFrequencyHz/self.samplingRate)*self.signalAmplitude
        elif self.mode == SignalGenerator.SignalMode.Square:
            if self.__cnt % self.__halfPeriodSamples == 0:
                self.__direction = self.__direction * -1
            for i in range(self.channelCount):
                data[i] = self.__direction * self.signalAmplitude
        elif self.mode == SignalGenerator.SignalMode.Sawtooth:
            for i in range(self.channelCount):
                data[i] = self.__cnt % self.__periodSamples * self.__k- self.signalAmplitude
        elif self.mode == SignalGenerator.SignalMode.Triangle:
            if self.__cnt % self.__halfPeriodSamples == 0:
                self.__direction = self.__direction * -1
            for i in range(self.channelCount):
                if self.__direction  > 0:
                    data[i] = self.__cnt % self.__halfPeriodSamples * self.__k - self.signalAmplitude
                else:
                    data[i] = self.__cnt % self.__halfPeriodSamples * -self.__k+ self.signalAmplitude
        for i in range(self.channelCount):
            if i % 2 == 1:
                data[i] = data[i] * -1
        for i in range(self.channelCount):
                data[i] += self.signalOffset
        
        self.__cnt += 1
        self.write(0, np.array([data]))