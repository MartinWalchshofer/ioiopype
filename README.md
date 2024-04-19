# IOIOpype
 IOIOpype is processing framework for realtime applications written in python. Data is propergated between Nodes that can be connected via Streams. Nodes can be input nodes 'INode', output nodes 'ONode' or input and output nodes 'IONode'. Algorithms and signal processing pipelines can be prototyped easily by combining multiple nodes.

## Supported Devices
- Unicorn Hybrid Black (g.tec medical engineering GmbH)
- Unicorn Hybrid Black Simulator

## INodes
- ConsoleLog - Writes received data to the console
- ToWorkspace - Propagates data to the main thread via event
- FramePlot - Plots a data frame
- SamplePlot - Plots time series data
- CSV Logger - Logs data to csv files
- UDP Receiver - Receives data via UDP

## IONodes
- Buffer - Buffers data with a defined window size and overlap
- PWelch - Calculates a Pwelch spectrum from a frame
- Downsample - Samples a data frame down by a given factor
- OffsetCorrection - Removes the offset from a data frame
- ButterworthFilter - Applies a butterworth filter to a sample based signal
- ButterworthFiltFilt - Applies a butterworth filter to a frame as filtfilt
- ToSample - Slices and forwards a data frame into samples
- Log - Applies a logarithm to the input signal (ln, log10, 10*log10)
- Square - Squares the input signal
- Sqrt - Calsulates the square root of the input signal
- Mux - Concatenates multiple signals into one
- Operation - Adds, Subtracts, Multiplies, Divides or applies a matrix multiplication
- Serialize - Serialized data into json or xml strings
- Deserialize - Deserializes XML or JSON serialized data

## ONodes
- Constant - forwards constant data with a defined sampling rate
- NoiseGenerator - Generates gaussian noise as a timeseries signal.
- SignalGenerator - Generates sample based timeseries signals. Sine, Square, Sawtooth and Triangle signals can be generated
- Frame - Allows to send a data frame to INodes
- UDPSender - Sends data via UDP

## Supported platforms

| Windows    | Linux    | Mac  |
| :--------- |:---------| :----|

## Install ioiopype from PyPi

```pip install ioiopype```

## Unicorn Hybrid Black - Acquisition and data visualization example

This example shows how to connect to a 'Unicorn - The Brain Interface' device and establish a data acquisition. Raw data acquired from the device is filtered with Butterworth IIR filters and visualized using a timeseries plot. Additionally the raw spectrum is calculated using a pwelch spectrum. The spectrum is visualized using a frame plot.

```python
from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

use_device_simulator = True #Use device simulator (True) or real device (False)
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
```

![Unicorn Hybrid Black - Acquisition and data visualization example](https://github.com/MartinWalchshofer/ioiopype/blob/main/img/example1.png)

## Contact
Support this project: [![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/MartinWalchshofer)<br>
Join IOIOPype on [Discord](https://discord.gg/pKEumyD9)<br>
Contact: ```mwalchsoferyt at gmail dot com```