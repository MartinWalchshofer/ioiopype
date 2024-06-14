import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio
import numpy as np
app = QApplication(sys.argv)

samplingRate = 500
numberOfChannels = 3

sig1 = ioio.Constant(samplingRate, np.array([[0, 0, 1]]))
sig2 = ioio.NoiseGenerator(samplingRate, 3, 0, 0.1)
add1 = ioio.Operation(2, ioio.Operation.Type.Add)

sig3 = ioio.Constant(samplingRate, np.array([[0, 0, 0]]))
sig4 = ioio.NoiseGenerator(samplingRate, 3, 0, 5)
add2 = ioio.Operation(2, ioio.Operation.Type.Add)

sp1 = ioio.SamplePlot(3, samplingRate, 6.66, 2)
sp2 = ioio.SamplePlot(3, samplingRate, 6.66, 100)
sp3 = ioio.SamplePlot(1, samplingRate, 6.66, 2)

move = ioio.MovementDetector(0.1, 10)

sig1.connect(0, add1.InputStreams[0])
sig2.connect(0, add1.InputStreams[1])
add1.connect(0, move.InputStreams[0])
add1.connect(0, sp1.InputStreams[0])

sig3.connect(0, add2.InputStreams[0])
sig4.connect(0, add2.InputStreams[1])
add2.connect(0, move.InputStreams[1])
add2.connect(0, sp2.InputStreams[0])

move.connect(0, sp3.InputStreams[0])

sig1.start()
sig2.start()
sig3.start()
sig4.start()

app.exec()

sig1.stop()
sig2.stop()
sig3.stop()
sig4.stop()

sig1.disconnect(0, add1.InputStreams[0])
sig2.disconnect(0, add1.InputStreams[1])
add1.disconnect(0, move.InputStreams[0])
add1.disconnect(0, sp1.InputStreams[0])

sig3.disconnect(0, add2.InputStreams[0])
sig4.disconnect(0, add2.InputStreams[1])
add2.disconnect(0, move.InputStreams[1])
add2.disconnect(0, sp2.InputStreams[0])

move.disconnect(0, sp3.InputStreams[0])