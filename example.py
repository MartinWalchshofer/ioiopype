from ioiopype import DataGenerator, ConsoleLog, Buffer

#initialize nodes
samplingRate = 1
numberOfChannels = 8
bufferSizeInSamples = 10
bufferOverlapInSamples = 8

dg = DataGenerator(samplingRate, numberOfChannels)
buf = Buffer(numberOfChannels, bufferSizeInSamples, bufferOverlapInSamples)
cl1 = ConsoleLog()
cl2 = ConsoleLog()
cl3 = ConsoleLog()

#connect nodes
#connect output 0 of data generator to input 0 of buffer
dg.connect(0, buf.InputStreams[0])
#connect output 0 of buffer to input 0 of console log 1
buf.connect(0, cl1.InputStreams[0])
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
#disconnect output 0 of buffer frum input 0 of console log 1
buf.disconnect(0, cl1.InputStreams[0])
#disconnect output 1 of data generator from input 0 of console log 2
dg.disconnect(1, cl2.InputStreams[0]) 
#disconnect output 1 of data generator from input 0 of console log 3
dg.disconnect(1, cl3.InputStreams[0]) 

#stop data generation
dg.stop()