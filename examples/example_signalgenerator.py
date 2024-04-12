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
amplitude = 50
frequency = 0.5
offset = 50
siggen1 = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, amplitude, frequency, offset)
siggen2 = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Sawtooth, amplitude, frequency, offset)
siggen3 = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Square, amplitude, frequency, offset)
siggen4 = ioio.SignalGenerator(fs, numberOfChannels, ioio.SignalGenerator.SignalMode.Triangle, amplitude, frequency, offset)
mux = ioio.Mux(4)
buf = ioio.Buffer(numberOfChannels * 4, 4 * fs, 4 * fs - 25)
pw = ioio.PWelch(fs)
fp = ioio.FramePlot(samplingRate=4)
sp = ioio.SamplePlot(numberOfChannels * 4, fs, 5.5, (amplitude + offset)*2)

#build ioiopype
siggen1.connect(0, mux.InputStreams[0])
siggen2.connect(0, mux.InputStreams[1])
siggen3.connect(0, mux.InputStreams[2])
siggen4.connect(0, mux.InputStreams[3])
mux.connect(0, buf.InputStreams[0])
buf.connect(0, pw.InputStreams[0])
pw.connect(0, fp.InputStreams[0])
mux.connect(0, sp.InputStreams[0])

siggen1.start()
siggen2.start()
siggen3.start()
siggen4.start()

app.exec()

siggen1.stop()
siggen2.stop()
siggen3.stop()
siggen4.stop()

#disconnect ioiopype
siggen1.disconnect(0, mux.InputStreams[0])
siggen2.disconnect(0, mux.InputStreams[1])
siggen3.disconnect(0, mux.InputStreams[2])
siggen4.disconnect(0, mux.InputStreams[3])
mux.disconnect(0, buf.InputStreams[0])
buf.disconnect(0, pw.InputStreams[0])
pw.disconnect(0, fp.InputStreams[0])
mux.disconnect(0, sp.InputStreams[0])
