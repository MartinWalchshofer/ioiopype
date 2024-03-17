from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from ..utilities.butterworth import butterworth
import numpy as np
import scipy.signal as sp
import json

class ButterworthFiltFilt(IONode):
    def __init__(self, type, samplingRate, order, cutoffFrequencies):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Frame)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.Frame)))
        self.type = type
        self.samplingRate = samplingRate
        self.order = order
        self.cutoffFrequencies = cutoffFrequencies
        self.b, self.a = butterworth(type, samplingRate, order, cutoffFrequencies)

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
            "type": self.type.name,
            "samplingRate": self.samplingRate,
            "order": self.order,
            "cutoffFrequencies": self.cutoffFrequencies,
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
            self.write(0, sp.filtfilt(self.b, self.a, data, axis=0, method="gust"))  
             