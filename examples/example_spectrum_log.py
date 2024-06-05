'''This example shows how to connect to a 'Unicorn - The Brain Interface' device, calculate and visualize a pwelch spectrum and log data '''

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
spectrumBufferS = 4
buf = ioio.Buffer(device.NumberOfEEGChannels, spectrumBufferS * device.SamplingRateInHz, spectrumBufferS * device.SamplingRateInHz - 25) # frame size and overlap
pw = ioio.PWelch(device.SamplingRateInHz)
fp = ioio.FramePlot(samplingRate=spectrumBufferS)
buf2 = ioio.Buffer(device.NumberOfEEGChannels, spectrumBufferS * device.SamplingRateInHz, spectrumBufferS * device.SamplingRateInHz - 25) # frame size and overlap
pw2 = ioio.PWelch(device.SamplingRateInHz)
fp2 = ioio.FramePlot(samplingRate=spectrumBufferS)
hp = ioio.ButterworthFilter(ioio.FilterType.Highpass, device.SamplingRateInHz, 2, [6]) #2nd order 6Hz increase cutoff frequency to remove LF artifacts (no ssvep below 6hz)
lp = ioio.ButterworthFilter(ioio.FilterType.Lowpass, device.SamplingRateInHz, 4, [50]) #4th order 50Hz adjust lowpass frequency to desired cutoff
n50 = ioio.ButterworthFilter(ioio.FilterType.Notch, device.SamplingRateInHz, 4, [48, 52]) #4th order 50Hz power line hum EU
n60 = ioio.ButterworthFilter(ioio.FilterType.Notch, device.SamplingRateInHz, 4, [58, 62]) #4th order 60Hz power line hum US
sp = ioio.SamplePlot(device.NumberOfEEGChannels, device.SamplingRateInHz, 6, 100) # 6s +-100uV
csvRaw = ioio.CSVLogger(1)
csv = ioio.CSVLogger(1)

#build ioiopype
device.connect(0, buf.InputStreams[0])
buf.connect(0, pw.InputStreams[0])
pw.connect(0, fp.InputStreams[0])
device.connect(0, csvRaw.InputStreams[0])

device.connect(0, n50.InputStreams[0])
n50.connect(0, n60.InputStreams[0])
n60.connect(0, hp.InputStreams[0])
hp.connect(0, lp.InputStreams[0])
lp.connect(0, sp.InputStreams[0])
lp.connect(0, csv.InputStreams[0])
lp.connect(0, buf2.InputStreams[0])
buf2.connect(0, pw2.InputStreams[0])
pw2.connect(0, fp2.InputStreams[0])

csvRaw.open(dir + '/data_raw.csv', header='EEG1,EEG2,EEG3,EEG4,EEG5,EEG6,EEG7,EEG8')
csv.open(dir + '/data_filt.csv', header='EEG1,EEG2,EEG3,EEG4,EEG5,EEG6,EEG7,EEG8')

app.exec()

csvRaw.close()
csv.close()

#disconnect ioiopype
device.disconnect(0, buf.InputStreams[0])
buf.disconnect(0, pw.InputStreams[0])
pw.disconnect(0, fp.InputStreams[0])
device.disconnect(0, csvRaw.InputStreams[0])

device.disconnect(0, n50.InputStreams[0])
n50.disconnect(0, n60.InputStreams[0])
n60.disconnect(0, hp.InputStreams[0])
hp.disconnect(0, lp.InputStreams[0])
lp.disconnect(0, sp.InputStreams[0])
lp.disconnect(0, csv.InputStreams[0])
lp.disconnect(0, buf2.InputStreams[0])
buf2.disconnect(0, pw2.InputStreams[0])
pw2.disconnect(0, fp2.InputStreams[0])

#close device
del device