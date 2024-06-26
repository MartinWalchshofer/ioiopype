from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from PySide6.QtCore import QObject, Signal, Slot 
import pyqtgraph as pg
import numpy as np
import time

class FramePlot(INode):
    UpdateRateHz = 20

    class QTFramePlot(QObject):
        updateSignal = Signal(np.ndarray)

        def __init__(self, samplingRate=1, displayedAmplitude=[]):
            super(FramePlot.QTFramePlot, self).__init__()

            self.samplingRate = samplingRate
            self.plotWidget = pg.plot(title="frame plot")
            if len(displayedAmplitude) == 2:
                self.plotWidget.setYRange(displayedAmplitude[0], displayedAmplitude[1], 0)
            elif len(displayedAmplitude) == 1:
                self.plotWidget.setYRange(-displayedAmplitude[0], displayedAmplitude[0], 0)

            self.x = None
            self.numberOfChannels = 0
            self.items = []

            self.updateSignal.connect(self.update_plot)

        @Slot(np.ndarray)
        def update_plot(self, y):
            if y is not None:
                if self.x is None or self.x.shape[0] != y.shape[0]:
                    self.x = np.linspace(1, y.shape[0], y.shape[0])
                    self.x = np.divide(self.x,self.samplingRate)

                self.numberOfChannels = y.shape[1]
                if len(self.items) is not self.numberOfChannels:
                    for i in range(0, self.numberOfChannels):
                        self.items.append(pg.PlotCurveItem())
                        self.plotWidget.addItem(self.items[i])
                for i in range(0, self.numberOfChannels):
                    self.items[i].setData(x=self.x, y= y[:,i])

    def __init__(self, samplingRate=1, displayedAmplitude=[]):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'data', StreamInfo.Datatype.Frame)))
        
        self.__timestamp = 0
        self.__dT = 0
        self.dTS = 1/self.UpdateRateHz
        self.qto = FramePlot.QTFramePlot(samplingRate, displayedAmplitude)

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:   
            self.y =  data
        timestamp = time.time()
        self.__dT += timestamp - self.__timestamp
        self.__timestamp = timestamp
        if self.__dT >= self.dTS:
            self.qto.updateSignal.emit(data)
            self.__dT = 0