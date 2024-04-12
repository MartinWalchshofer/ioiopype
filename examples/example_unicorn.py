'''This example shows how to connect to a 'Unicorn - The Brain Interface' device, calculate and visualize a pwelch spectrum '''

import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

use_device_simulator = False #Use device simulator (True) or real device (False)
if use_device_simulator:
    device = ioio.UnicornSimulator('UN-0000.00.00')
else:
    device = ioio.Unicorn('UN-2023.02.15') #Enter your device serial here

#initialize processing nodes
buf = ioio.Buffer(device.NumberOfEEGChannels, 4 * device.SamplingRateInHz, 4 * device.SamplingRateInHz - 25)
pw = ioio.PWelch(device.SamplingRateInHz)
fp = ioio.FramePlot(samplingRate=4)
hp = ioio.ButterworthFilter(ioio.FilterType.Highpass, device.SamplingRateInHz, 2, [2])
lp = ioio.ButterworthFilter(ioio.FilterType.Lowpass, device.SamplingRateInHz, 4, [30])
n50 = ioio.ButterworthFilter(ioio.FilterType.Notch, device.SamplingRateInHz, 4, [48, 52])
n60 = ioio.ButterworthFilter(ioio.FilterType.Notch, device.SamplingRateInHz, 4, [58, 62])
sp = ioio.SamplePlot(device.NumberOfEEGChannels, device.SamplingRateInHz, 6, 100)

#build ioiopype
device.connect(0, buf.InputStreams[0])
buf.connect(0, pw.InputStreams[0])
pw.connect(0, fp.InputStreams[0])

device.connect(0, n50.InputStreams[0])
n50.connect(0, n60.InputStreams[0])
n60.connect(0, hp.InputStreams[0])
hp.connect(0, lp.InputStreams[0])
lp.connect(0, sp.InputStreams[0])

app.exec()

#disconnect ioiopype
device.disconnect(0, buf.InputStreams[0])
buf.disconnect(0, pw.InputStreams[0])
pw.disconnect(0, fp.InputStreams[0])

device.disconnect(0, n50.InputStreams[0])
n50.disconnect(0, n60.InputStreams[0])
n60.disconnect(0, hp.InputStreams[0])
hp.disconnect(0, lp.InputStreams[0])
lp.disconnect(0, sp.InputStreams[0])

#close device
del device