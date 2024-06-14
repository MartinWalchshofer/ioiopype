from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
import json

class MovementDetector(IONode):
    def __init__(self, accRangeG, gyrRangeDegS):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'acc', StreamInfo.Datatype.Sample)))
        self.add_i_stream(IStream(StreamInfo(1, 'gyr', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'movement', StreamInfo.Datatype.Sample)))
        self.accRangeG = accRangeG
        self.gyrRangeDegS = gyrRangeDegS

    def __del__(self):
        super().__del__()

    def __dict__(self):
        istreams = []
        for i in range(0,len(self.InputStreams)):
            istreams.append(self.InputStreams[i].StreamInfo.__dict__())
        ostreams = []
        for i in range(0,len(self.OutputStreams)):
            ostreams.append(self.OutputStreams[i].StreamInfo.__dict__())
        return {
            "name": self.__class__.__name__,
            "accRangeG": self.accRangeG,
            "gyrRangeDegS": self.gyrRangeDegS,
            "i_streams": istreams,
            "o_streams": ostreams
        }
    
    def __str__(self):
        return json.dumps(self.__dict__(), indent=4)

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)

    def update(self):
        acc = self.InputStreams[0].read()
        gyr = self.InputStreams[1].read()
        
        if acc.shape[1] != 3:
            raise ValueError('Accelerometer must feature 3 dimensions')
        
        if gyr.shape[1] != 3:
            raise ValueError('Gyroscope must feature 3 dimensions')

        totalAcc = np.sqrt(np.sum(acc**2, axis=1))
        totalGyr = np.sqrt(np.sum(gyr**2, axis=1))
        movement = np.where((totalAcc <= 1-self.accRangeG) | (totalAcc >= 1+self.accRangeG) | (totalGyr >= self.gyrRangeDegS), 1, 0)      
        self.OutputStreams[0].write(movement)             