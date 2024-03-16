'''This example builds a realtime pipeline with different processing steps, plots and console outputs'''

import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiopype as ioio

#initialize nodes
samplingRate = 250
numberOfChannels = 8
signalAmplitude = 10
signalFrequency = 10
signalOffset = 100
signalNoise = 5
timesSamplingRate = 4
bufferSizeInSamples = samplingRate * timesSamplingRate
bufferOverlapInSamples = samplingRate * timesSamplingRate - 25
displayedTimeRangeS = 6
displayedAmplitude = 100

#define nodes
dg = ioio.DataGenerator(samplingRate, numberOfChannels, signalAmplitude=signalAmplitude, signalFrequencyHz=signalFrequency, signalOffset=signalOffset, signalNoise=signalNoise)
buf = ioio.Buffer(numberOfChannels, bufferSizeInSamples, bufferOverlapInSamples)
oc = ioio.OffsetCorrection(100, mode=ioio.OffsetCorrection.OffsetCorrectionMode.Linear)
pw = ioio.PWelch(samplingRate)
fp1 = ioio.FramePlot(samplingRate=4, displayedAmplitude=[0, 10])
fp2 = ioio.FramePlot(samplingRate=samplingRate, displayedAmplitude=[-50, 50] )
sp = ioio.SamplePlot(numberOfChannels, samplingRate, displayedTimeRangeS, displayedAmplitude)
cl1 = ioio.ConsoleLog()
cl2 = ioio.ConsoleLog()
cl3 = ioio.ConsoleLog()

#connect nodes
dg.connect(0, buf.InputStreams[0])
buf.connect(0, cl1.InputStreams[0])
buf.connect(0, oc.InputStreams[0])
oc.connect(0, pw.InputStreams[0])
pw.connect(0, fp1.InputStreams[0])
oc.connect(0, fp2.InputStreams[0])
dg.connect(0, sp.InputStreams[0])
dg.connect(1, cl2.InputStreams[0]) 
dg.connect(1, cl3.InputStreams[0]) 

#start data generation
dg.start()

print('Press ENTER to terminate the script')
input()

#disconnect nodes
dg.disconnect(0, buf.InputStreams[0])
buf.disconnect(0, cl1.InputStreams[0])
buf.disconnect(0, oc.InputStreams[0])
oc.disconnect(0, pw.InputStreams[0])
pw.disconnect(0, fp1.InputStreams[0])
oc.disconnect(0, fp2.InputStreams[0])
dg.disconnect(0, sp.InputStreams[0])
dg.disconnect(1, cl2.InputStreams[0]) 
dg.disconnect(1, cl3.InputStreams[0]) 

#stop data generation
dg.stop()