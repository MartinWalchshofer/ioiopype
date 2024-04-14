import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiopype as ioio
import numpy as np

samplingRate = 100
v = ioio.NoiseGenerator(samplingRate, 3, 0, 1)
m2 = ioio.Constant(samplingRate, np.random.rand(3,3))
m3 = ioio.Constant(samplingRate, np.random.rand(3,3))
m = ioio.Operation(3, ioio.Operation.Type.MatrixMultiply)
c = ioio.ConsoleLog()

v.connect(0, m.InputStreams[0])
m2.connect(0, m.InputStreams[1])
m3.connect(0, m.InputStreams[2])
m.connect(0, c.InputStreams[0])

v.start()
m2.start()
m3.start()

input('Press ENTER to terminate the application\n')

v.stop()
m2.stop()
m3.stop()

v.disconnect(0, m.InputStreams[0])
m2.disconnect(0, m.InputStreams[1])
m3.disconnect(0, m.InputStreams[2])
m.disconnect(0, c.InputStreams[0])
