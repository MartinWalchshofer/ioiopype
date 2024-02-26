from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
import numpy as np

class Downsample(IONode):
    def __init__(self, downsamplingFactor):
        super().__init__()
        self.add_i_stream(IStream(0, 'frame'))
        self.add_o_stream(OStream(0,'frame'))
        self.downsamplingFactor = downsamplingFactor

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            self.write(0, data[::self.downsamplingFactor,:]) 