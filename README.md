# IOIOpype
 IOIOpype is general purpose signal processing framework for realtime applications written in python. Data is proagated between Nodes that can be connected via Streams. Nodes can be input nodes 'INode', output nodes 'ONode' or input and output nodes 'IONode'. Algorithms and signal processing pipelines can be prototyped easily by combining multiple nodes.

## Examples

- [BLE HRV Example](/examples/example_ble_heart_rate_variability.py)
- [CSV Read](/examples/example_csv_read.py)
- [CSV Write](/examples/example_csv_write.py)
- [Data Acquisition](/examples/example_daq.py)
- [Elementwise Operation](/examples/example_elementwise_operation.py)
- [JSON UDP](/examples/example_json_udp.py)
- [Matrix Multiply](/examples/example_matrix_multiply.py)
- [Movement Detector](/examples/example_movement_detector.py)
- [Multiplex](/examples/example_multiplex.py)
- [Signal Genrerator](/examples/example_signalgenerator.py)
- [Spectrum Log](/examples/example_spectrum_log.py)
- [Timeseries Visualization](/examples/example_timeseries_visualization.py)

## Acquisition and data visualization example

```python
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

samplingRate = 500
channelCount = 2
sig1 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sine, 0.5, 2, 0)
sig2 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Triangle, 0.5, 2, 0)
sig3 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sawtooth, 0.5, 2, 0)
mux = ioio.Mux(3)

#initialize processing nodes
numberOfChannels = len(mux.InputStreams) * channelCount
sp2 = ioio.SamplePlot(numberOfChannels, samplingRate, 5.2, 1.5, displayMode=ioio.SamplePlot.DisplayMode.Continous)

#build ioiopype
sig1.connect(0, mux.InputStreams[0])
sig2.connect(0, mux.InputStreams[1])
sig3.connect(0, mux.InputStreams[2])
mux.connect(0, sp2.InputStreams[0])

sig1.start()
sig2.start()
sig3.start()

app.exec()

sig1.stop()
sig2.stop()
sig3.stop()

#disconnect ioiopype
sig1.disconnect(0, mux.InputStreams[0])
sig2.disconnect(0, mux.InputStreams[1])
sig3.disconnect(0, mux.InputStreams[2])
mux.disconnect(0, sp2.InputStreams[0])
```

![Data Acquisition Example](img/example1.png)

## INodes
### General Purpose
- [ConsoleLog](/ioiopype/common/i_nodes/console_log.py) - Writes received data to the console
- [ToWorkspace](/ioiopype/common/i_nodes/to_workspace.py) - Propagates data to the main thread via event
- [FramePlot](/ioiopype/desktop/i_nodes/frame_plot.py) - Plots a data frame
- [SamplePlot](/ioiopype/desktop/i_nodes/sample_plot.py) - Plots time series data
- [SpectrumPlot](/ioiopype/desktop/i_nodes/spectrum_plot.py) - Plots pwelch spectrum
- [CSV Logger](/ioiopype/common/i_nodes/csv_logger.py) - Logs data to csv files
- [UDP Sender](/ioiopype/common/i_nodes/udp_sender.py) - Sends data via UDP

## IONodes
### General Purpose
- Buffer - Buffers data with a defined window size and overlap
- PWelch - Calculates a Pwelch spectrum from a frame
- Downsample - Samples a data frame down by a given factor
- OffsetCorrection - Removes the offset from a data frame
- ButterworthFilter - Applies a butterworth filter to a sample based signal
- ButterworthFiltFilt - Applies a butterworth filter to a frame as filtfilt
- ToSample - Slices and forwards a data frame into samples
- Log - Applies a logarithm to the input signal (ln, log10, 10*log10)
- Square - Squares the input signal
- Sqrt - Calculates the square root of the input signal
- Mux - Concatenates multiple signals into one
- Operation - Adds, Subtracts, Multiplies, Divides or applies a matrix multiplication
- Serialize - Serialized data into json or xml strings
- Deserialize - Deserializes XML or JSON serialized data
- Transpose - Transposes an input matrix
- GetRange - Gets a range of a matrix

### Heart Rate Variability
- LFHF - Calculates LF and HF power as well as ratios from a HRV spectrum
- Poincare - Arranges a given time window of RR data for a poincare plot

### IMU
- MovementDetector - Uses Accelerometer and Gyroscope inputs to detect movement
- ComplementaryFilter - Applies a complementary filter to estimate orientation of a IMU sensor (not finished yet)

## ONodes
### General Purpose
- Constant - forwards constant data with a defined sampling rate
- Counter - A counter iterating with every sample
- NoiseGenerator - Generates gaussian noise as a timeseries signal.
- SignalGenerator - Generates sample based timeseries signals. Sine, Square, Sawtooth and Triangle signals can be generated
- Frame - Allows to send a data frame to INodes
- UDPSender - Sends data via UDP

### Pulse Sensor
- BLEHeartRate - Pulse Sensor supporting default Bluetooth LE Heart Rate Service
- BLEHeartRateSimulator - Simulates a 'BLEHeartRate' device

## Supported platforms

| Windows    | Linux    | Mac  |
| :--------- |:---------| :----|

## Install ioiopype from PyPi

```pip install ioiopype```

## Contact
Contact: ```mwalchsoferyt at gmail dot com```