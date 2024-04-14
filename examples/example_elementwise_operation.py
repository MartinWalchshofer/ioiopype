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
numberOfChannels = 2
amplitude = 0.5
frequency = 0.1
offset = 0.5
displayedTimeRange = 10.5
sigScale = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, amplitude, frequency, offset)
sp1 = ioio.SamplePlot(numberOfChannels, fs, displayedTimeRange, (amplitude + offset)*2)

frequency = 10
amplitude = 50
offset = 0
sigSin = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, amplitude, frequency, offset)
sp2 = ioio.SamplePlot(numberOfChannels, fs, displayedTimeRange, (amplitude + offset)*2)

sigNoise = ioio.NoiseGenerator(fs, numberOfChannels, 0, 10)
sp3 = ioio.SamplePlot(numberOfChannels, fs, displayedTimeRange, (amplitude + offset)*2)

add = ioio.ElementWiseOperation(2, ioio.ElementWiseOperation.Operation.Add)
mult = ioio.ElementWiseOperation(2, ioio.ElementWiseOperation.Operation.Multiply)
sp4 = ioio.SamplePlot(numberOfChannels, fs, displayedTimeRange, (amplitude + offset)*2)

#build ioiopype
sigScale.connect(0, sp1.InputStreams[0])
sigSin.connect(0, sp2.InputStreams[0])
sigNoise.connect(0, sp3.InputStreams[0])

sigSin.connect(0, add.InputStreams[0])
sigNoise.connect(0, add.InputStreams[1])
add.connect(0, mult.InputStreams[0])
sigScale.connect(0, mult.InputStreams[1])
mult.connect(0, sp4.InputStreams[0])

sigScale.start()
sigSin.start()
sigNoise.start()

app.exec()

sigScale.stop()
sigSin.stop()
sigNoise.stop()

#disconnect ioiopype
sigScale.disconnect(0, sp1.InputStreams[0])
sigSin.disconnect(0, sp2.InputStreams[0])
sigNoise.disconnect(0, sp3.InputStreams[0])

sigSin.disconnect(0, add.InputStreams[0])
sigNoise.disconnect(0, add.InputStreams[1])
add.disconnect(0, mult.InputStreams[0])
sigScale.disconnect(0, mult.InputStreams[1])
mult.disconnect(0, sp4.InputStreams[0])