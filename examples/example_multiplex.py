'''This example shows how to concatenate two signals into one using the 'Mux' node'''
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
m = ioio.Mux(2)
sp = ioio.SamplePlot(device.NumberOfAccChannels + device.NumberOfGyrChannels, device.SamplingRateInHz, 5.2, 1.5, displayMode=ioio.SamplePlot.DisplayMode.Continous)

#build ioiopype - connect signal 1 (ACC) and 2 (GYR) from unicorn to signal 0 and 1 of mux. Plot concatenated signal.
device.connect(1, m.InputStreams[0])
device.connect(2, m.InputStreams[1])
m.connect(0, sp.InputStreams[0])

app.exec()

#disconnect ioiopype
device.disconnect(1, m.InputStreams[0])
device.disconnect(2, m.InputStreams[1])
m.disconnect(0, sp.InputStreams[0])

#close device
del device