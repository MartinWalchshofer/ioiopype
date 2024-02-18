from ioiopype import DataGenerator, ConsoleLog

#initialize nodes
dg = DataGenerator(1, 8)
cl1 = ConsoleLog()
cl2 = ConsoleLog()
cl3 = ConsoleLog()

#connect nodes
dg.OutputStreams[0].connect(cl1.InputStreams[0])
dg.OutputStreams[1].connect(cl2.InputStreams[0])
dg.OutputStreams[1].connect(cl3.InputStreams[0])

#start data generation
dg.start()

print('Press ENTER to terminate the script')
input()

#disconnect nodes
dg.OutputStreams[0].disconnect(cl1.InputStreams[0])
dg.OutputStreams[1].disconnect(cl2.InputStreams[0])
dg.OutputStreams[1].disconnect(cl3.InputStreams[0])

#stop data generation
dg.stop()

#call destructor
cl1.__del__()
cl2.__del__()
cl3.__del__()