from ioiopype import DataGenerator, ConsoleLog

#initialize nodes
dg = DataGenerator(1, 8)
cl1 = ConsoleLog()
cl2 = ConsoleLog()
cl3 = ConsoleLog()

#connect nodes
dg.connect(0, cl1.InputStreams[0]) #connect output 0 of data generator to input 0 of console log 1
dg.connect(1, cl2.InputStreams[0]) #connect output 1 of data generator to input 0 of console log 2
dg.connect(1, cl3.InputStreams[0]) #connect output 1 of data generator to input 0 of console log 3

#start data generation
dg.start()

print('Press ENTER to terminate the script')
input()

#disconnect nodes
dg.disconnect(0, cl1.InputStreams[0]) #disconnect output 0 of data generator from input 0 of console log 1
dg.disconnect(1, cl2.InputStreams[0]) #disconnect output 1 of data generator from input 0 of console log 2
dg.disconnect(1, cl3.InputStreams[0]) #disconnect output 1 of data generator from input 0 of console log 3

#stop data generation
dg.stop()

#call destructor
cl1.__del__()
cl2.__del__()
cl3.__del__()