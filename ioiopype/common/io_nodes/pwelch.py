from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
import scipy.signal as sp
import json

class PWelch(IONode):
    def __init__(self, samplingRate):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Frame)))
        self.add_o_stream(OStream(StreamInfo(0, 'frequency', StreamInfo.Datatype.Frame)))
        self.add_o_stream(OStream(StreamInfo(1, 'spectrum', StreamInfo.Datatype.Frame)))
        self.samplingRate = samplingRate
        self.spectrum = None
        
        self.frequencies = None

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
            rows = data.shape[0]
            columns = data.shape[1]
            if self.spectrum is None:
                self.spectrum = np.zeros((rows// 2 + 1, columns))
            frequencies, self.spectrum = sp.welch(data, fs=self.samplingRate, window='hann' ,nperseg=rows, average='median', scaling='spectrum', axis=0)
            self.spectrum = np.sqrt(self.spectrum*2)
            self.write(0, np.array([frequencies]).transpose())
            self.write(1, self.spectrum)   