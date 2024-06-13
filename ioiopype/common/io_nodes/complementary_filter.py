from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from ..utilities.butterworth import butterworth
import numpy as np
import scipy.signal as sp
import json

class ComplementaryFilter(IONode):
    def __init__(self, alpha):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'acc', StreamInfo.Datatype.Sample)))
        self.add_i_stream(IStream(StreamInfo(1, 'gyr', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.Sample)))
        self.alpha

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
        data = []
        for i in range(0,len(self.InputStreams)):
            dataTmp = self.InputStreams[i].read()
            if dataTmp.ndim == 1:
                dataTmp = np.array([dataTmp])
            if dataTmp.ndim > 2:
                raise ValueError("Dimensions do not fit")
            data.append(dataTmp)
        
        #TODO NOT FINISHED YET
             