from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from ...common.utilities.overriding_buffer import OverridingBuffer
import pyqtgraph as pg
import numpy as np
from enum import Enum

class SamplePlot(INode):
    class DisplayMode(Enum):
        Overriding = 1
        Continous = 2

    def __init__(self, numberOfChannels, samplingRate, displayedTimeRangeS, amplitude, displayMode=DisplayMode.Overriding):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Sample)))
        self.numberOfChannels = numberOfChannels
        self.samplingRate = samplingRate
        self.displayedTimeRangeS = displayedTimeRangeS
        self.displayedTimeRangeSamples = samplingRate * displayedTimeRangeS
        self.x = np.linspace(1, self.displayedTimeRangeSamples, self.displayedTimeRangeSamples)
        self.x = np.divide(self.x,self.samplingRate)
        if displayMode is self.DisplayMode.Overriding:
            self.buffer = OverridingBuffer(self.displayedTimeRangeSamples , self.numberOfChannels, OverridingBuffer.OutputMode.NotAligned)
        else:
            self.buffer = OverridingBuffer(self.displayedTimeRangeSamples , self.numberOfChannels, OverridingBuffer.OutputMode.Aligned)
        self.offsets = []
        for i in range(0, self.numberOfChannels):
            if i % 2 == 0:
                self.offsets.append(amplitude * (numberOfChannels/2) - amplitude/2 - i*amplitude)
            else:
                self.offsets.append(amplitude * ((numberOfChannels/2)-0.5) - i*amplitude)

        self.plotWidget = pg.plot(title="sample plot")
        self.plotWidget.getPlotItem().hideAxis('left')
        self.items = []
        for i in range(0, self.numberOfChannels):
            self.items.append(pg.PlotCurveItem())
            self.plotWidget.addItem(self.items[i])

        minMaxAmplitude = 0
        if self.numberOfChannels % 2 == 0:
            minMaxAmplitude = (self.numberOfChannels/2) * amplitude 
            self.plotWidget.setYRange(-1 * minMaxAmplitude,minMaxAmplitude, 0)
        else:
            minMaxAmplitude = (amplitude/2)+((self.numberOfChannels/2)-0.5)*amplitude
            self.plotWidget.setYRange(-1 * minMaxAmplitude, minMaxAmplitude, 0)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(round(1/25))

    def __del__(self):
        super().__del__()
        self.timer.stop()

    def update_plot(self):
        data = self.buffer.getFrame()
        for i in range(0, self.numberOfChannels):
            self.items[i].setData(x=self.x, y= data[:,i] + self.offsets[i])

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            for row in data:
                self.buffer.setData(data)