import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiopype as ioio

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

updateRateHz = 1
sp = ioio.SamplePlot(1, updateRateHz, 33.33, 150)

device.connect(0, sp.InputStreams[0])

input('Press ENTER to terminate the application')

device.disconnect(0, sp.InputStreams[0])

del device