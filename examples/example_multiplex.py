'''This example shows how to concatenate two signals into one using the 'Mux' node'''
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

samplingRate = 500
numberOfChannels = 3
sig1 = ioio.SignalGenerator(samplingRate, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, 1, 5, 0)
sig2 = ioio.SignalGenerator(samplingRate, numberOfChannels, ioio.SignalGenerator.SignalMode.Triangle, 1, 10, 0)
mux = ioio.Mux(2)

#initialize processing nodes
sp = ioio.SamplePlot(numberOfChannels * len(mux.InputStreams) , samplingRate, 5.2, 4, displayMode=ioio.SamplePlot.DisplayMode.Continous)

sig1.connect(0, mux.InputStreams[0])
sig2.connect(0, mux.InputStreams[1])
mux.connect(0, sp.InputStreams[0])

sig1.start()
sig2.start()

app.exec()

sig1.stop()
sig2.stop()

#disconnect ioiopype
sig1.disconnect(0, mux.InputStreams[0])
sig2.disconnect(0, mux.InputStreams[1])
mux.disconnect(0, sp.InputStreams[0])