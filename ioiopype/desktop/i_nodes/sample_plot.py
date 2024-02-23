from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...common.utilities.overriding_buffer import OverridingBuffer
import pyqtgraph as pg
import numpy as np

class SamplePlot(INode):
    def __init__(self, numberOfChannels, samplingRate, displayedTimeRangeS):
        super().__init__()
        self.add_i_stream(IStream(0, 'in'))
        self.numberOfChannels = numberOfChannels
        self.samplingRate = samplingRate
        self.displayedTimeRangeS = displayedTimeRangeS
        self.displayedTimeRangeSamples = samplingRate * displayedTimeRangeS
        self.x = np.linspace(1, self.displayedTimeRangeSamples, self.displayedTimeRangeSamples)
        self.x = np.divide(self.x,self.samplingRate)
        self.buffer = OverridingBuffer(self.displayedTimeRangeSamples , self.numberOfChannels)
        
        self.plotWidget = pg.plot(title="sample plot")
        self.plotWidget.getPlotItem().hideAxis('left')
        self.items = []
        for i in range(0, self.numberOfChannels):
            self.items.append(pg.PlotCurveItem())
            self.plotWidget.addItem(self.items[i])
        
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(round(1/25))

    def __del__(self):
        super().__del__()
        self.timer.stop()

    def update_plot(self):
        data = self.buffer.getFrame()
        for i in range(0, self.numberOfChannels):
            self.items[i].setData(x=self.x, y= data[:,i])

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            for row in data:
                self.buffer.setData(data)