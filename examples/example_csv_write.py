import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiopype as ioio

samplingRate = 500
numberOfChannels = 2
sig1 = ioio.SignalGenerator(samplingRate, numberOfChannels, ioio.SignalGenerator.SignalMode.Sine, 5, 10, 0)
sig2 = ioio.SignalGenerator(samplingRate, numberOfChannels, ioio.SignalGenerator.SignalMode.Triangle, 5, 10, 0)
sig3 = ioio.SignalGenerator(samplingRate, numberOfChannels, ioio.SignalGenerator.SignalMode.Sawtooth, 5, 10, 0)
mux = ioio.Mux(3)

#create csv logger for every output stream the unicorn provides
csv = ioio.CSVLogger(len(mux.OutputStreams))

#open file
csv.open(dir + '/test.csv', header='CH1,CH2,CH3,CH4,CH5,CH6')

sig1.connect(0, mux.InputStreams[0])
sig2.connect(0, mux.InputStreams[1])
sig3.connect(0, mux.InputStreams[2])
for i in range(0, len(mux.OutputStreams)):
    mux.connect(i, csv.InputStreams[i])

sig1.start()
sig2.start()
sig3.start()

input('Press ENTER to terminate the application\n')

sig1.stop()
sig2.stop()
sig3.stop()

#close file
csv.close()

#disconnect streams
sig1.disconnect(0, mux.InputStreams[0])
sig2.disconnect(0, mux.InputStreams[1])
sig3.disconnect(0, mux.InputStreams[2])
for i in range(0, len(mux.OutputStreams)):
    mux.disconnect(i, csv.InputStreams[i])