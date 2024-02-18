from ioiopype import DataGenerator, ConsoleLog

#initialize nodes
dg = DataGenerator(1, 8)
cl = ConsoleLog()

#connect nodes
dg.OutputStreams[1].connect(cl.InputStreams[0])

#start data generation
dg.start()