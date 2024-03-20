from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from ...common.utilities.overriding_buffer import OverridingBuffer
from enum import Enum
from PyQt6 import QtCore
import pyqtgraph as pg
import numpy as np
import time

class QTSamplePlot(QtCore.QObject):
    updateSignal = QtCore.pyqtSignal(OverridingBuffer)

    def __init__(self, numberOfChannels, samplingRate, displayedTimeRangeSamples, amplitude):
        super(QtCore.QObject, self).__init__()

        self.numberOfChannels = numberOfChannels
        self.samplingRate = samplingRate
        
        self.x = np.linspace(1, int(displayedTimeRangeSamples), int(displayedTimeRangeSamples))
        self.x = np.divide(self.x,samplingRate)

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
        
        self.updateSignal.connect(self.update_plot)
    
    def update_plot(self, buffer):
        data = buffer.getFrame()
        for i in range(0, self.numberOfChannels):
            self.items[i].setData(x=self.x, y= data[:,i] + self.offsets[i])

class SamplePlot(INode):
    UpdateRateHz = 20

    class DisplayMode(Enum):
        Overriding = 1
        Continous = 2

    def __init__(self, numberOfChannels, samplingRate, displayedTimeRangeS, amplitude, displayMode=DisplayMode.Overriding):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Sample)))
        
        displayedTimeRangeSamples = samplingRate * displayedTimeRangeS
        if displayMode is self.DisplayMode.Overriding:
            self.buffer = OverridingBuffer(displayedTimeRangeSamples , numberOfChannels, OverridingBuffer.OutputMode.NotAligned)
        else:
            self.buffer = OverridingBuffer(displayedTimeRangeSamples , numberOfChannels, OverridingBuffer.OutputMode.Aligned)

        self.__timestamp = 0
        self.__dT = 0
        self.dTS = 1/self.UpdateRateHz
        self.qto = QTSamplePlot(numberOfChannels, samplingRate, displayedTimeRangeSamples, amplitude)
        
    def __del__(self):
        super().__del__()

    def update(self):
        data = None        
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            for row in data:
                self.buffer.setData(data)
        timestamp = time.time()
        self.__dT += timestamp - self.__timestamp
        self.__timestamp = timestamp
        if self.__dT >= self.dTS:
            self.qto.updateSignal.emit(self.buffer)
            self.__dT = 0