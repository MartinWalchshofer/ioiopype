from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ..utilities.butterworth import Butterworth
import numpy as np

class ButterworthIIR(IONode):

    def __init__(self, type, samplingRate, order, cutoffFrequencies):
        super().__init__()
        self.add_i_stream(IStream(0, 'sample'))
        self.add_o_stream(OStream(0,'sample'))
        bw = Butterworth(type, samplingRate, order, cutoffFrequencies)
        self.b, self.a = bw.get_coefficients()

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             for row in data:
                raise NotImplementedError("TBD")