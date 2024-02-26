from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
import numpy as np
from enum import Enum

class OffsetCorrection(IONode):
    class OffsetCorrectionMode(Enum):
        Constant = 1
        Linear = 2
        #TODO ADD SPLINE MODE

    def __init__(self, numberOfSamples, mode=OffsetCorrectionMode.Linear):
        super().__init__()
        self.add_i_stream(IStream(0, 'frame'))
        self.add_o_stream(OStream(0,'frame'))
        self.numberOfSamples = numberOfSamples
        self.mode = mode

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            if self.mode is self.OffsetCorrectionMode.Constant:
                self.write(0, data - np.mean(data[:self.numberOfSamples, :], axis=0))
            elif self.mode is self.OffsetCorrectionMode.Linear:
                first_avg = np.mean(data[:self.numberOfSamples, :], axis=0)
                last_avg = np.mean(data[-self.numberOfSamples:, :], axis=0)
                k = (last_avg - first_avg) / (data.shape[0] - self.numberOfSamples)
                d = first_avg
                detrend_matrix = np.zeros_like(data)
                for i in range(data.shape[1]):
                    detrend_matrix[:, i] = data[:, i] - (k[i] * np.arange(data.shape[0]) + d[i])
                self.write(0, detrend_matrix) 