'''This example shows how to connect to use a signal generator, visualize data and calculate a pwelch spectum'''

import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

#initialize processing nodes
fs = 100
numberOfChannels = 8
amplitude = 0.5
frequency = 0.1
offset = 0.5
siggenScale = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, amplitude, frequency, offset)
sp1 = ioio.SamplePlot(numberOfChannels, fs, 10, (amplitude + offset)*2)

numberOfChannels = 8
frequency = 10
amplitude = 50
offset = 0
siggenSig = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, amplitude, frequency, offset)
sp2 = ioio.SamplePlot(numberOfChannels, fs, 10, (amplitude + offset)*2)

add = ioio.ElementWiseOperation(2, ioio.ElementWiseOperation.Operation.DotMultiply)
sp3 = ioio.SamplePlot(numberOfChannels, fs, 5.5, (amplitude + offset)*2)

#build ioiopype
siggenScale.connect(0, sp1.InputStreams[0])
siggenSig.connect(0, sp2.InputStreams[0])
siggenScale.connect(0, add.InputStreams[0])
siggenSig.connect(0, add.InputStreams[1])
add.connect(0, sp3.InputStreams[0])

siggenScale.start()
siggenSig.start()

app.exec()

siggenScale.stop()
siggenSig.stop()

#disconnect ioiopype
siggenScale.disconnect(0, sp1.InputStreams[0])
siggenSig.disconnect(0, sp2.InputStreams[0])
siggenScale.disconnect(0, add.InputStreams[0])
siggenSig.disconnect(0, add.InputStreams[1])
add.disconnect(0, sp3.InputStreams[0])