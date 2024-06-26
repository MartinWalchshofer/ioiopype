from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from PySide6.QtCore import QObject, Signal, Slot 
import pyqtgraph as pg
import numpy as np
import time

class SpectrumPlot(INode):
    UpdateRateHz = 20

    class QTFramePlot(QObject):
        updateSignal = Signal(np.ndarray)

        def __init__(self, title, xlim=[], ylim=[]):
            super(SpectrumPlot.QTFramePlot, self).__init__()
            self.plotWidget = pg.plot(title=title)
            if len(xlim) == 2:
                self.plotWidget.setXRange(xlim[0], xlim[1], 0)
            if len(ylim) == 2:
                self.plotWidget.setYRange(ylim[0], ylim[1], 0)
            elif len(ylim) == 1:
                self.plotWidget.setYRange(-ylim[0], ylim[0], 0)

            self.numberOfChannels = 0
            self.items = []

            self.updateSignal.connect(self.update_plot)

        @Slot(np.ndarray)
        def update_plot(self, data):
            if len(data) != 2:
                raise ValueError('Invalid Data')
            frequency = data[0]
            spectrum = data[1]
            if frequency is not None and spectrum is not None:
                self.numberOfChannels = spectrum.shape[1]
                if len(self.items) is not self.numberOfChannels:
                    for i in range(0, self.numberOfChannels):
                        self.items.append(pg.PlotCurveItem())
                        self.plotWidget.addItem(self.items[i])
                for i in range(0, self.numberOfChannels):
                    self.items[i].setData(x=frequency[:,0], y= spectrum[:,i])

    def __init__(self, title = 'spectrum plot', xlim=[], ylim=[]):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'frequency', StreamInfo.Datatype.Frame)))
        self.add_i_stream(IStream(StreamInfo(1, 'spectrum', StreamInfo.Datatype.Frame)))
        
        self.__timestamp = 0
        self.__dT = 0
        self.dTS = 1/self.UpdateRateHz
        self.qto = SpectrumPlot.QTFramePlot(title, xlim, ylim)

    def __del__(self):
        super().__del__()

    def update(self):
        frequency = self.InputStreams[0].read()
        spectrum = self.InputStreams[1].read()

        timestamp = time.time()
        self.__dT += timestamp - self.__timestamp
        self.__timestamp = timestamp
        if self.__dT >= self.dTS:
            self.qto.updateSignal.emit([frequency, spectrum])
            self.__dT = 0