import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import ioiopype as ioio
import json
samplingRate = 250
numberOfChannels = 8
signalAmplitude = 10
signalFrequency = 10
signalOffset = 100
signalNoise = 10
timesSamplingRate = 4
bufferSizeInSamples = samplingRate * timesSamplingRate
bufferOverlapInSamples = samplingRate * timesSamplingRate - 25

nodes = []
nodes.append(ioio.DataGenerator(samplingRate, numberOfChannels, signalAmplitude=signalAmplitude, signalFrequencyHz=signalFrequency, signalOffset=signalOffset, signalNoise=signalNoise))
nodes.append(ioio.Buffer(numberOfChannels, bufferSizeInSamples, bufferOverlapInSamples))
nodes.append(ioio.PWelch(samplingRate))

dgjson = str(nodes[0])
dg = ioio.DataGenerator.initialize(dgjson)

with open(SCRIPT_DIR + 'output.json', 'w') as json_file:
    json.dump(nodes, json_file)


connections = []

ioioPype = ioio.IOIOPypeBuilder(SCRIPT_DIR + "/test_realtime_pipe2.json")

'''TODO NOT FINISHED YET'''