#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ..utilities.realtime_clock import RealtimeClock
import numpy as np
import json

class CSVReader(ONode, RealtimeClock):
    def __init__(self, samplingRate, loop=True):
        super().__init__()
        super(ONode, self).__init__(samplingRate)
        self.add_o_stream(OStream(StreamInfo(0, 'data', StreamInfo.Datatype.Sample)))
        self.__samplingRate = samplingRate
        self.__loop = loop
        self.__csvfile = None
        self.__filepath = None
        self.start()

    def __del__(self):
        self.stop()
        super().__del__()
        super(ONode, self).__del__()

    def __dict__(self):
        ostreams = []
        for i in range(0,len(self.OutputStreams)):
            ostreams.append(self.OutputStreams[i].StreamInfo.__dict__())
        return {
            "name": self.__class__.__name__,
            "samplingRate": self.__samplingRate,
            "loop": self.__loop,
            "o_streams": ostreams
        }
    
    def __str__(self):
        return json.dumps(self.__dict__(), indent=4)

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)

    def open(self, filepath):
        if self.__csvfile is None:
            self.__csvfile = open(filepath, 'r')
            self.__filepath = filepath
            self.__csvfile.readline()
        else:
            raise ValueError('File already open')

    def close(self):
        if self.__csvfile is not None:
            self.__csvfile.close()
            self.__csvfile = None

    def update(self):
        if self.__csvfile is not None:
            eof = False
            line = self.__csvfile.readline()
            if line == '':
                eof = True
            
            if eof is False:
                lineSplit = list(map(float, line.split(',')))
                self.write(0, np.array(lineSplit).reshape(1, len(lineSplit)))
                
            if eof and self.__loop is True:
                self.close()
                self.open(self.__filepath)