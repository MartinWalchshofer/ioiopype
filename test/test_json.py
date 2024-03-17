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

'''streaminfo -> json / json -> streaminfo'''
si = str(ioio.StreamInfo(1, 'test', ioio.StreamInfo.Datatype.Sample))
print(si)
sids = ioio.StreamInfo.initialize(si)

'''node -> json / json -> node'''
b = str(ioio.Buffer(8, fs, fs-10))
print(b)
bds = ioio.Buffer.initialize(b)

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

'''nodes to json'''
for node in nodes:
    print(str(nodes[1]))

'''nodes to file'''
with open(dir + '/output.json', 'w') as json_file:
    json.dump(nodes, json_file, default=lambda o: o.__dict__(), indent=4)

'''file to nodes'''
with open(dir + '/output.json', 'r') as json_file:
    node_dict = json.load(json_file)

