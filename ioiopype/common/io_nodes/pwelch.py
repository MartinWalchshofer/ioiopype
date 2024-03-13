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
        self.add_o_stream(OStream(StreamInfo(0, 'spectrum', StreamInfo.Datatype.Frame)))
        self.add_o_stream(OStream(StreamInfo(1, 'frequency', StreamInfo.Datatype.Frame)))
        self.samplingRate = samplingRate
        self.spectrum = None
        
        self.frequencies = None

    def __del__(self):
        super().__del__()

    def __dict__(self):
        return {
            "name": self.__class__.__name__,
            "samplingRate": self.samplingRate,
        }
    
    def __str__(self):
        return json.dumps(self.__dict__())

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
            frequencies, self.spectrum = sp.welch(data, fs=self.samplingRate, window='hamming' ,nperseg=rows, average='median', scaling='spectrum', axis=0)
            self.spectrum = np.sqrt(self.spectrum)
            self.write(0, self.spectrum)   
            self.write(1, frequencies)      