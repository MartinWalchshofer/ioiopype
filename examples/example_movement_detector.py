import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

samplingRate = 500
numberOfChannels = 3
sig1 = ioio.SignalGenerator(samplingRate, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, 1, 1, 0)
sig2 = ioio.SignalGenerator(samplingRate, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, 1, 1, 0)
sp1 = ioio.SamplePlot(3, samplingRate, 6.66, 2)
sp2 = ioio.SamplePlot(3, samplingRate, 6.66, 2)
sp3 = ioio.SamplePlot(1, samplingRate, 6.66, 2)

move = ioio.MovementDetector(0.1, 10)

sig1.connect(0, move.InputStreams[0])
sig2.connect(0, move.InputStreams[1])
sig1.connect(0, sp1.InputStreams[0])
sig2.connect(0, sp2.InputStreams[0])
move.connect(0, sp3.InputStreams[0])

sig1.start()
sig2.start()

app.exec()

sig1.stop()
sig2.stop()

sig1.disconnect(0, move.InputStreams[0])
sig2.disconnect(0, move.InputStreams[1])
sig1.disconnect(0, sp1.InputStreams[0])
sig2.disconnect(0, sp2.InputStreams[0])
move.disconnect(0, sp3.InputStreams[0])