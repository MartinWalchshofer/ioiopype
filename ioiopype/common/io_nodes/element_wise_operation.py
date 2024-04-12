from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from enum import Enum
import numpy as np
import json

class ElementWiseOperation(IONode):
    class Operation(Enum):
        DotAdd = 1
        DotSubtract = 2
        DotMultiply = 3
        DotDivide = 4

    def __init__(self, numberOfInputSignals, operation):
        super().__init__()
        for i in range(0, numberOfInputSignals):
            self.add_i_stream(IStream(StreamInfo(i, 'in' + str(i+1), StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.Sample)))    
        self.operation = operation
        
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
            "operation": self.operation.name,
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
        data = []
        for i in range(0,len(self.InputStreams)):
            dataTmp = self.InputStreams[i].read()
            if dataTmp.ndim == 1:
                dataTmp = np.array([dataTmp])
            if dataTmp.ndim > 2:
                raise ValueError("Dimensions do not fit")
            data.append(dataTmp)
        for i in range(0, len(data)-1):
            if data[i].shape[0] != data[i+1].shape[0] or data[i].shape[1] != data[i+1].shape[1]:
                raise ValueError("Inconsistent matrix dimensions.")
        
        dataOut = data[0]
        for i in range(1, len(data)):
            if self.operation is ElementWiseOperation.Operation.DotAdd:
                dataOut = dataOut + data[i]
            elif self.operation is ElementWiseOperation.Operation.DotSubtract:
                dataOut = dataOut - data[i]
            elif self.operation is ElementWiseOperation.Operation.DotMultiply:
                dataOut = dataOut * data[i]
            elif self.operation is ElementWiseOperation.Operation.DotDivide:
                dataOut = dataOut / data[i]
        self.write(0, dataOut)