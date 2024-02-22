from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
import pyqtgraph as pg

class FramePlot(INode):
    def __init__(self, samplingRate=1):
        super().__init__()
        self.add_i_stream(IStream(0, 'in'))
        self.samplingRate = samplingRate
        self.plotHandle = None

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             if self.plotHandle is None:
                #TODO
                self.plotHandle = pg.plot(x, y, pen='r')