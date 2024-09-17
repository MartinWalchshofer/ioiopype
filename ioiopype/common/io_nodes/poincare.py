from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
import json

class Poincare(IONode):
    def __init__(self, windowSize):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'RR', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'Poincare', StreamInfo.Datatype.Frame)))
        self.windowSize = windowSize
        self.__cnt = 0
        self.__buf = np.zeros((self.windowSize, 2))
        
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
            "windowSize": self.windowSize,
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
        rr = self.InputStreams[0].read()
        iprev = (self.__cnt - 1) % self.windowSize
        icur = self.__cnt % self.windowSize
        self.__buf[icur, 0] = rr
        self.__buf[iprev, 1] = self.__buf[icur, 0]
        
        if self.__cnt < self.windowSize and self.__cnt > 0:
            self.write(0, self.__buf[0:self.__cnt, :])
        if self.__cnt >= self.windowSize and self.__cnt > 0:
            self.write(0, self.__buf)
        self.__cnt += 1