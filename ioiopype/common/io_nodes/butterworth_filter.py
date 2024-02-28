from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ..utilities.butterworth import butterworth
import scipy.signal as sp

class ButterworthFilter(IONode):

    def __init__(self, type, samplingRate, order, cutoffFrequencies):
        super().__init__()
        self.add_i_stream(IStream(0, 'sample'))
        self.add_o_stream(OStream(0,'sample'))
        self.b, self.a = butterworth(type, samplingRate, order, cutoffFrequencies)
        self.zi = None

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             if self.zi is None:
                 self.zi = sp.lfilter_zi(self.b, self.a)
             for row in data:
                row_filt, zf = sp.lfilter(self.b, self.a, row,axis=0, zi=self.zi)
                self.zi = zf
                self.write(0, row_filt)