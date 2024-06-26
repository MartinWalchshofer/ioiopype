import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

use_device_simulator = False #Use device simulator (True) or real device (False)

#on devices discovered event / prints discovered devices to the console
discovered_devices = []
def on_devices_discovered(devices):
    global discovered_devices
    cnt = 0
    discovered_devices = devices
    for device in discovered_devices:
        print('#' + str(cnt) + ': ' + device)
        cnt = cnt+1

#start scanning for devices
if use_device_simulator:
    ioio.BLEHeartRateSimulator.add_devices_discovered_eventhandler(on_devices_discovered)
    ioio.BLEHeartRateSimulator.start_scanning()
else:
    ioio.BLEHeartRate.add_devices_discovered_eventhandler(on_devices_discovered)
    ioio.BLEHeartRate.start_scanning()

#select device
selectedId = int(input('Select device by id:\n'))

#stop scanning for devices
if use_device_simulator:
    ioio.BLEHeartRateSimulator.remove_devices_discovered_eventhandler()
    ioio.BLEHeartRateSimulator.stop_scanning()
else:
    ioio.BLEHeartRate.remove_devices_discovered_eventhandler()
    ioio.BLEHeartRate.stop_scanning()

if use_device_simulator:
    device = ioio.BLEHeartRateSimulator(discovered_devices[selectedId])
else:
    device = ioio.BLEHeartRate(discovered_devices[selectedId])

updateRateHz = 1000
spectrumWindowSizeS = 120
spectrumWindowOverlapS = 119
buf = ioio.Buffer(1, spectrumWindowSizeS * updateRateHz, spectrumWindowOverlapS * updateRateHz )
spec = ioio.PWelch(updateRateHz)
specplot = ioio.SpectrumPlot(xlim=[0, 0.5])
sp = ioio.SamplePlot(1, updateRateHz, 60*5, [30,90], displayMode=ioio.SamplePlot.DisplayMode.Continous, title='heart rate')

device.connect(2, sp.InputStreams[0])
device.connect(3, buf.InputStreams[0])
buf.connect(0, spec.InputStreams[0])
spec.connect(0, specplot.InputStreams[0])
spec.connect(1, specplot.InputStreams[1])

app.exec()

device.disconnect(2, sp.InputStreams[0])
device.disconnect(3, buf.InputStreams[0])
buf.disconnect(0, spec.InputStreams[0])
spec.disconnect(0, specplot.InputStreams[0])
spec.disconnect(1, specplot.InputStreams[1])

del device