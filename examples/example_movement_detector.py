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
mux = ioio.Mux(2)