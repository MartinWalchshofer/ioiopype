'''This example shows how to connect to a 'Unicorn - The Brain Interface' device, calculate and visualize a pwelch spectrum '''

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

#initialize nodes
device = ioio.Unicorn(discovered_devices[selectedId])
buf = ioio.Buffer(device.NumberOfEEGChannels, 4 * device.SamplingRateInHz, 4 * device.SamplingRateInHz - 25)
pw = ioio.PWelch(device.SamplingRateInHz)
fp = ioio.FramePlot(samplingRate=4)

#build ioiopype
device.connect(0, buf.InputStreams[0])
buf.connect(0, pw.InputStreams[0])
pw.connect(0, fp.InputStreams[0])

input('Press any key to terminate the application\n')

#disconnect ioiopype
device.disconnect(0, buf.InputStreams[0])
buf.disconnect(0, pw.InputStreams[0])
pw.disconnect(0, fp.InputStreams[0])

#close device
del device