from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
import pyqtgraph as pg
import numpy as np

class FramePlot(INode):
    def __init__(self, samplingRate=1):
        super().__init__()
        self.add_i_stream(IStream(0, 'in'))
        self.samplingRate = samplingRate
        self.plotWidget = pg.plot(title="frame plot")

        self.x = None
        self.y = None
        self.numberOfChannels = 0
        self.items = []
        
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(round(1/50))

    def __del__(self):
        super().__del__()

        self.timer.stop()

    def update_plot(self):
        self.numberOfChannels = self.y.shape[1]
        if len(self.items) is not self.numberOfChannels:
            for i in range(0, self.numberOfChannels):
                self.items.append(pg.PlotCurveItem())
                self.plotWidget.addItem(self.items[i])
        for i in range(0, self.numberOfChannels):
                self.items[i].setData(x=self.x, y= self.y[:,i]+i*20)#tbd

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            if self.x is None or self.x.shape[0] != data.shape[0]:
                self.x = np.linspace(1, data.shape[0], data.shape[0])
                self.x = np.divide(self.x,self.samplingRate)
            self.y =  data