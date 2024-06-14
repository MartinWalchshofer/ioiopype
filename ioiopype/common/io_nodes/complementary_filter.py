from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from ..utilities.butterworth import butterworth
import numpy as np
import scipy.signal as sp
import json
import math

class ComplementaryFilter(IONode):
    def __init__(self, samplingRate, alpha):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'acc', StreamInfo.Datatype.Sample)))
        self.add_i_stream(IStream(StreamInfo(1, 'gyr', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.Sample)))
        self.alpha = alpha
        self.samplingRate = samplingRate

    def __del__(self):
        super().__del__()

    def __dict__(self):
        istreams = []
        for i in range(0,len(self.InputStreams)):
            istreams.append(self.InputStreams[i].StreamInfo.__dict__())
        ostreams = []
        for i in range(0,len(self.OutputStreams)):
            ostreams.append(self.OutputStreams[i].StreamInfo.__dict__())
        return {
            "name": self.__class__.__name__,
            "samplingRate": self.samplingRate,
            "alpha": self.alpha,
            "i_streams": istreams,
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
        acc = self.InputStreams[0].read()
        gyr = self.InputStreams[1].read()

        acc_roll = math.atan2(acc[1],acc[2])
        acc_pitch = math.atan2(-acc[0],math.sqrt(acc[1]**2+acc[2]**2))
        acc_yaw = 0

        