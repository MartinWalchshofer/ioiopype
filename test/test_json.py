import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiopype as ioio
import json

fs = 250
fclp = [10]
fchp = [80]
fcn = [48,52]

nodes = {
    1: ioio.ButterworthFilter(ioio.FilterType.Highpass, fs, 2, fclp),
    2: ioio.ButterworthFilter(ioio.FilterType.Lowpass, fs, 4, fchp),
    3: ioio.ButterworthFilter(ioio.FilterType.Notch, fs, 4, fcn),
    4: ioio.Buffer(8, fs, fs-10),
    5: ioio.Downsample(4),
    6: ioio.OffsetCorrection(100, ioio.OffsetCorrection.OffsetCorrectionMode.Linear),
    7: ioio.PWelch(fs),
    8: ioio.ToSample()
}

print(str(nodes[1]))
print(str(nodes[2]))
print(str(nodes[3]))
#nodes.append(ioio.Buffer(numberOfChannels, bufferSizeInSamples, bufferOverlapInSamples))
#nodes.append(ioio.PWelch(samplingRate))

'''TODO
NODES AND CONNECTIONS (PIPE) TO JSON
JSON TO NODES AND CONNECTIONS'''

print(str(nodes[1]))
print(str(nodes[1].__dict__))
print(json.dumps(nodes, default=lambda o: str(o), indent=4))


dictjson = json.dumps(nodes, default=lambda o: str(o), indent=4)
nodes1 = json.loads(dictjson)

with open(dir + '/output.json', 'w') as json_file:
    json.dump(nodes, json_file, default=lambda o: str(o), indent=4)

#serialize one node
dgjson = str(nodes[1])
dg = ioio.ButterworthFilter.initialize(dgjson)

connections = []

ioioPype = ioio.IOIOPypeBuilder(dir + "/test_realtime_pipe2.json")

'''TODO NOT FINISHED YET'''