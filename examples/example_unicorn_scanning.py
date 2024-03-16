'''This example shows how to connect to a 'Unicorn - The Brain Interface' device, calculate and visualize a pwelch spectrum '''

import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiopype as ioio

use_device_simulator = True #Use device simulator (True) or real device (False)

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
    ioio.UnicornSimulator.add_devices_discovered_eventhandler(on_devices_discovered)
    ioio.UnicornSimulator.start_scanning()
else:
    ioio.Unicorn.add_devices_discovered_eventhandler(on_devices_discovered)
    ioio.Unicorn.start_scanning()

#select device
selectedId = int(input('Select device by id:\n'))

#stop scanning for devices
if use_device_simulator:
    ioio.UnicornSimulator.remove_devices_discovered_eventhandler()
    ioio.UnicornSimulator.stop_scanning()
else:
    ioio.Unicorn.remove_devices_discovered_eventhandler()
    ioio.Unicorn.stop_scanning()

if use_device_simulator:
    device = ioio.UnicornSimulator(discovered_devices[selectedId])
else:
    device = ioio.Unicorn(discovered_devices[selectedId])

#initialize nodes
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

input('Press any key to terminate the application\n')

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