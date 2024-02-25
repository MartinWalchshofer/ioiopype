from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
import numpy as np
import scipy.signal as sp

class PWelch(IONode):
    def __init__(self, samplingRate):
        super().__init__()
        self.add_i_stream(IStream(0, 'frame'))
        self.add_o_stream(OStream(0,'spectrum'))
        self.add_o_stream(OStream(1,'frequency'))
        self.samplingRate = samplingRate
        self.spectrum = None
        
        self.frequencies = None

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            rows = data.shape[0]
            columns = data.shape[1]
            if self.spectrum is None:
                self.spectrum = np.zeros((rows// 2 + 1, columns))
            frequencies, self.spectrum = sp.welch(data, fs=self.samplingRate, nperseg=rows, average='median', scaling='spectrum', axis=0)
            self.spectrum = np.sqrt(self.spectrum)
            self.write(0, self.spectrum)   
            self.write(1, frequencies)      