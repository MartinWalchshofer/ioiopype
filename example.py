from ioiopype import DataGenerator, ConsoleLog, Buffer, FramePlot, SamplePlot

#initialize nodes
samplingRate = 250
numberOfChannels = 8
bufferSizeInSamples = 250 * 4
bufferOverlapInSamples = 250 * 4 - 250
displayedTimeRangeS = 6
displayedAmplitude = 100

dg = DataGenerator(samplingRate, numberOfChannels)
buf = Buffer(numberOfChannels, bufferSizeInSamples, bufferOverlapInSamples)
fp1 = FramePlot(samplingRate=samplingRate)
fp2 = FramePlot(samplingRate=samplingRate)
sp = SamplePlot(numberOfChannels, samplingRate, displayedTimeRangeS, displayedAmplitude)
cl1 = ConsoleLog()
cl2 = ConsoleLog()
cl3 = ConsoleLog()

#connect nodes
#connect output 0 of data generator to input 0 of buffer
dg.connect(0, buf.InputStreams[0])
#connect output 0 of buffer to input 0 of console log 1
buf.connect(0, cl1.InputStreams[0])
#connect output 0 of buffer to input 0 of frame plot 1
buf.connect(0, fp1.InputStreams[0])
#connect output 0 of buffer to input 0 of frame plot 2
buf.connect(0, fp2.InputStreams[0])
#connect output 0 of data generator to input 0 of sample plot
dg.connect(0, sp.InputStreams[0])
#connect output 1 of data generator to input 0 of console log 2
dg.connect(1, cl2.InputStreams[0]) 
#connect output 1 of data generator to input 0 of console log 3
dg.connect(1, cl3.InputStreams[0]) 

#start data generation
dg.start()

print('Press ENTER to terminate the script')
input()

#disconnect nodes
#disconnect output 0 of data generator from input 0 of buffer
dg.disconnect(0, buf.InputStreams[0])
#disconnect output 0 of buffer frum input 0 from console log 1
buf.disconnect(0, cl1.InputStreams[0])
#disconnect output 0 of buffer to input 0 from frame plot 1
buf.disconnect(0, fp1.InputStreams[0])
#disconnect output 0 of buffer to input 0 from frame plot 2
buf.disconnect(0, fp2.InputStreams[0])
#disconnect output 0 of data generator to input 0 from sample plot
dg.disconnect(0, sp.InputStreams[0])
#disconnect output 1 of data generator from input 0 from console log 2
dg.disconnect(1, cl2.InputStreams[0]) 
#disconnect output 1 of data generator from input 0 from console log 3
dg.disconnect(1, cl3.InputStreams[0]) 

#stop data generation
dg.stop()