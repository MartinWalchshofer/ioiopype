#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ..utilities.realtime_clock import RealtimeClock
import numpy as np
import json

class Counter(ONode, RealtimeClock):
    def __init__(self, samplingRate, channelCount, maxVal):
        super().__init__()
        super(ONode, self).__init__(samplingRate)
        self.add_o_stream(OStream(StreamInfo(0, 'data', StreamInfo.Datatype.Sample)))
        self.samplingRate = samplingRate
        self.channelCount = channelCount
        self.maxVal = maxVal
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
            "maxVal": self.maxVal,
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
        self.write(0, np.full((1, self.channelCount), self.__cnt % self.maxVal))
        self.__cnt += 1