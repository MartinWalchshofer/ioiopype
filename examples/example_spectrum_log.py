import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

channelCount = 2
samplingRate = 500
sig1 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sine, 30, 10, 0)
sig2 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sine, 30, 100, 0)
sig3 = ioio.SignalGenerator(samplingRate, channelCount, ioio.SignalGenerator.SignalMode.Sine, 30, 200, 0)
mux = ioio.Mux(3)

#initialize processing nodes
spectrumBufferS = 4
numberOfChannels = len(mux.InputStreams) * channelCount
buf = ioio.Buffer(numberOfChannels, spectrumBufferS * samplingRate, spectrumBufferS * samplingRate - 25) # frame size and overlap
pw = ioio.PWelch(samplingRate)
fp = ioio.FramePlot(samplingRate=spectrumBufferS)
buf2 = ioio.Buffer(numberOfChannels, spectrumBufferS * samplingRate, spectrumBufferS * samplingRate - 25) # frame size and overlap
pw2 = ioio.PWelch(samplingRate)
fp2 = ioio.FramePlot(samplingRate=spectrumBufferS)
hp = ioio.ButterworthFilter(ioio.FilterType.Highpass, samplingRate, 2, [6])
lp = ioio.ButterworthFilter(ioio.FilterType.Lowpass, samplingRate, 4, [150])
n50 = ioio.ButterworthFilter(ioio.FilterType.Notch, samplingRate, 4, [98, 102])
spraw = ioio.SamplePlot(numberOfChannels, samplingRate, 6, 100)
spfilt = ioio.SamplePlot(numberOfChannels, samplingRate, 6, 100)
csvRaw = ioio.CSVLogger(1)
csv = ioio.CSVLogger(1)

#build ioiopype
sig1.connect(0, mux.InputStreams[0])
sig2.connect(0, mux.InputStreams[1])
sig3.connect(0, mux.InputStreams[2])
mux.connect(0, buf.InputStreams[0])
buf.connect(0, pw.InputStreams[0])
pw.connect(0, fp.InputStreams[0])
mux.connect(0, csvRaw.InputStreams[0])
mux.connect(0, spraw.InputStreams[0])
mux.connect(0, n50.InputStreams[0])
n50.connect(0, hp.InputStreams[0])
hp.connect(0, lp.InputStreams[0])
lp.connect(0, spfilt.InputStreams[0])
lp.connect(0, csv.InputStreams[0])
lp.connect(0, buf2.InputStreams[0])
buf2.connect(0, pw2.InputStreams[0])
pw2.connect(0, fp2.InputStreams[0])

csvRaw.open(dir + '/data_raw.csv', header='CH1,CH2,CH3,CH4,CH5,CH6')
csv.open(dir + '/data_filt.csv', header='CH1,CH2,CH3,CH4,CH5,CH6')

sig1.start()
sig2.start()
sig3.start()

app.exec()

sig1.stop()
sig2.stop()
sig3.stop()

csvRaw.close()
csv.close()

#disconnect ioiopype
sig1.disconnect(0, mux.InputStreams[0])
sig2.disconnect(0, mux.InputStreams[1])
sig3.disconnect(0, mux.InputStreams[2])
mux.disconnect(0, buf.InputStreams[0])
buf.disconnect(0, pw.InputStreams[0])
pw.disconnect(0, fp.InputStreams[0])
mux.disconnect(0, csvRaw.InputStreams[0])
mux.connect(0, spraw.InputStreams[0])
mux.disconnect(0, n50.InputStreams[0])
n50.disconnect(0, hp.InputStreams[0])
hp.disconnect(0, lp.InputStreams[0])
lp.disconnect(0, spfilt.InputStreams[0])
lp.disconnect(0, csv.InputStreams[0])
lp.disconnect(0, buf2.InputStreams[0])
buf2.disconnect(0, pw2.InputStreams[0])
pw2.disconnect(0, fp2.InputStreams[0])