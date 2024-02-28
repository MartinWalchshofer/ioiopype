from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ..utilities.butterworth import butterworth
import numpy as np
import scipy.signal as sp

class ButterworthFiltFilt(IONode):

    def __init__(self, type, samplingRate, order, cutoffFrequencies):
        super().__init__()
        self.add_i_stream(IStream(0, 'frame'))
        self.add_o_stream(OStream(0, 'frame'))
        self.b, self.a = butterworth(type, samplingRate, order, cutoffFrequencies)

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            self.write(0, sp.filtfilt(self.b, self.a, data, axis=0, method="gust"))  
             