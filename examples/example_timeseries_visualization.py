'''This example shows how timeseries data can be be visualized in different ways using a sample plot'''

import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

samplingRate = 500
channelCount = 2
sig1 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sine, 0.5, 2, 0)
sig2 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Triangle, 0.5, 2, 0)
sig3 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sawtooth, 0.5, 2, 0)
mux = ioio.Mux(3)

#initialize processing nodes
numberOfChannels = len(mux.InputStreams) * channelCount
sp1 = ioio.SamplePlot(numberOfChannels, samplingRate, 5.2, 1.5, displayMode=ioio.SamplePlot.DisplayMode.Overriding)
sp2 = ioio.SamplePlot(numberOfChannels, samplingRate, 5.2, 1.5, displayMode=ioio.SamplePlot.DisplayMode.Continous)

#build ioiopype
sig1.connect(0, mux.InputStreams[0])
sig2.connect(0, mux.InputStreams[1])
sig3.connect(0, mux.InputStreams[2])
mux.connect(0, sp1.InputStreams[0])
mux.connect(0, sp2.InputStreams[0])

sig1.start()
sig2.start()
sig3.start()

app.exec()

sig1.stop()
sig2.stop()
sig3.stop()

#disconnect ioiopype
sig1.disconnect(0, mux.InputStreams[0])
sig2.disconnect(0, mux.InputStreams[1])
sig3.disconnect(0, mux.InputStreams[2])
mux.disconnect(0, sp1.InputStreams[0])
mux.disconnect(0, sp2.InputStreams[0])