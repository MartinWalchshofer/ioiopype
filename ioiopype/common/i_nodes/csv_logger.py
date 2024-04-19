
from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
import json

class CSVLogger(INode):
    def __init__(self, numberOfStreams):
        super().__init__()
        for i in range(0, numberOfStreams):
            self.add_i_stream(IStream(StreamInfo(i, 'data' + str(i), StreamInfo.Datatype.Sample)))
        self.__csvfile = None
        np.set_printoptions(threshold=np.inf)
        np.set_printoptions(linewidth=np.inf)

    def __del__(self):
        super().__del__()

    def __dict__(self):
        istreams = []
        for i in range(0,len(self.InputStreams)):
            istreams.append(self.InputStreams[i].StreamInfo.__dict__())
        return {
            "name": self.__class__.__name__,
            "numberOfStreams": len(istreams),
            "i_streams": istreams,
        }
    
    def __str__(self):
        return json.dumps(self.__dict__(), indent=4)

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)

    def open(self, filepath, header=''):
        if self.__csvfile is None:
            self.__csvfile = open(filepath, 'w')
            if len(header) > 0:
                self.__csvfile.write(header + '\n')
        else:
            raise ValueError('File already open')

    def close(self):
        if self.__csvfile is not None:
            self.__csvfile.close()
            self.__csvfile = None
        
    def update(self):
        for i in range (0, len(self.InputStreams)):
            data = self.InputStreams[i].read()
            if data.ndim == 1:
                data = np.array([data])
            if data.ndim > 2:
                raise ValueError("Dimensions do not fit")
            s =np.array2string(data, formatter={'float':lambda x: "%.5f" % x}, separator=",")
            s = s[2:-2]
            if self.__csvfile is not None:
                self.__csvfile.write(s)
                if i >= len(self.InputStreams) -1:
                    self.__csvfile.write('\n')
                else:
                    self.__csvfile.write(',')