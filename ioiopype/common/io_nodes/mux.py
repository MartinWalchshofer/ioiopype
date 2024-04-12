from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
import json

class Mux(IONode):

    def __init__(self, numberOfInputSignals):
        super().__init__()
        for i in range(0, numberOfInputSignals):
            self.add_i_stream(IStream(StreamInfo(i, 'in' + str(i+1), StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.Sample)))    
        
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
            "numberOfInputSignals": len(self.InputStreams),
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
        for i in range(0, len(data)-1):
            if data[i].shape[0] != data[i+1].shape[0]:
                raise ValueError("Inconsistent matrix dimensions. All multiplexed signals must have the same number of rows.")
        self.write(0,np.concatenate(data, axis=1))