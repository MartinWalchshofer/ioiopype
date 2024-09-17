from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
import json

class LFHF(IONode):
    def __init__(self):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'frequency', StreamInfo.Datatype.Frame)))
        self.add_i_stream(IStream(StreamInfo(1, 'spectrum', StreamInfo.Datatype.Frame)))
        self.add_o_stream(OStream(StreamInfo(0, 'LF', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'HF', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(2, 'LF/HF', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(3, 'LF Ratio Normalized', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(4, 'HF Ratio Normalized', StreamInfo.Datatype.Sample)))

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
        frequency = self.InputStreams[0].read()
        spectrum = self.InputStreams[1].read()

        lfi = np.where((frequency >= 0.04) & (frequency < 0.15))[0]
        hfi = np.where((frequency >= 0.15) & (frequency < 0.4))[0]

        lfp=np.trapz(spectrum[lfi,0])
        hfp=np.trapz(spectrum[hfi,0])

        self.write(0, np.array([[lfp]]))
        self.write(1, np.array([[hfp]]))  
        self.write(2, np.array([[lfp/hfp]]))  
        self.write(3, np.array([[lfp/(lfp+hfp)-0.5]]))  
        self.write(4, np.array([[hfp/(lfp+hfp)-0.5]]))  