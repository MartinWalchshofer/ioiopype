'''This example shows how timeseries data can be be visualized in different ways using a sample plot'''
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

use_device_simulator = True #Use device simulator (True) or real device (False)
if use_device_simulator:
    device = ioio.UnicornSimulator('UN-0000.00.00')
else:
    device = ioio.Unicorn('UN-2023.02.15') #Enter your device serial here

#initialize processing nodes
sp1 = ioio.SamplePlot(device.NumberOfAccChannels, device.SamplingRateInHz, 5.2, 1.5, displayMode=ioio.SamplePlot.DisplayMode.Overriding)
sp2 = ioio.SamplePlot(device.NumberOfAccChannels, device.SamplingRateInHz, 5.2, 1.5, displayMode=ioio.SamplePlot.DisplayMode.Continous)

#build ioiopype
device.connect(1, sp1.InputStreams[0])
device.connect(1, sp2.InputStreams[0])

app.exec()

#disconnect ioiopype
device.disconnect(1, sp1.InputStreams[0])
device.disconnect(1, sp2.InputStreams[0])

#close device
del device