from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
from enum import Enum
import json
class OffsetCorrection(IONode):
    class OffsetCorrectionMode(Enum):
        Constant = 1
        Linear = 2
        #TODO ADD SPLINE MODE

    def __init__(self, numberOfSamples, mode=OffsetCorrectionMode.Linear):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Frame)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.Frame)))
        self.numberOfSamples = numberOfSamples
        self.mode = mode

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
            "numberOfSamples": self.numberOfSamples,
            "mode": self.mode.name,
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
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            if self.mode is self.OffsetCorrectionMode.Constant or self.mode == self.OffsetCorrectionMode.Constant.name:
                self.write(0, data - np.mean(data[:self.numberOfSamples, :], axis=0))
            elif self.mode is self.OffsetCorrectionMode.Linear or self.mode == self.OffsetCorrectionMode.Linear.name:
                first_avg = np.mean(data[:self.numberOfSamples, :], axis=0)
                last_avg = np.mean(data[-self.numberOfSamples:, :], axis=0)
                k = (last_avg - first_avg) / (data.shape[0] - self.numberOfSamples)
                d = first_avg
                detrend_matrix = np.zeros_like(data)
                for i in range(data.shape[1]):
                    detrend_matrix[:, i] = data[:, i] - (k[i] * np.arange(data.shape[0]) + d[i])
                self.write(0, detrend_matrix) 