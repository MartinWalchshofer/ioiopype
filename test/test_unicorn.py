import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import ioiopype as ioio

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
ioio.Unicorn.add_devices_discovered_eventhandler(on_devices_discovered)
ioio.Unicorn.start_scanning()

#select device
selectedId = int(input('Select device by id:\n'))

#stop scanning for devices
ioio.Unicorn.remove_devices_discovered_eventhandler()
ioio.Unicorn.stop_scanning()

#open device
print('selected: ' + discovered_devices[selectedId])
device = ioio.Unicorn(discovered_devices[selectedId])
input('Press any key to terminate the application\n')

#close device
del device