import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)
samplingRate = 100
channelCount = 8
amplitude = 100
frequency = 1.33
offset=0
sg = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sine, amplitude, frequency, offset)
scope_sent = ioio.SamplePlot(channelCount, samplingRate, 5.5, (amplitude + offset)*2)
s = ioio.Serialize('data', ioio.Serialize.Mode.Json)
us = ioio.UDPSender('127.0.0.1', 5005)
ur = ioio.UDPReceiver('127.0.0.1', 5005)
ds = ioio.Deserialize('data', ioio.Deserialize.Mode.Json)
scope_received = ioio.SamplePlot(channelCount, samplingRate, 5.5, (amplitude + offset)*2)

sg.connect(0, s.InputStreams[0])
s.connect(0, us.InputStreams[0])
sg.connect(0, scope_sent.InputStreams[0])

ur.connect(0, ds.InputStreams[0])
ds.connect(0, scope_received.InputStreams[0])

sg.start()

app.exec()

sg.stop()

sg.disconnect(0, s.InputStreams[0])
s.disconnect(0, us.InputStreams[0])
sg.disconnect(0, scope_sent.InputStreams[0])

ur.disconnect(0, ds.InputStreams[0])
ds.disconnect(0, scope_received.InputStreams[0])