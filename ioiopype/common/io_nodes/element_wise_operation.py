from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
from enum import Enum
import numpy as np
import json

class ElementWiseOperation(IONode):
    class Operation(Enum):
        Add = 1
        Subtract = 2
        Multiply = 3
        Divide = 4

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
        
        dataOut = data[0]
        for i in range(1, len(data)):
            if self.operation is ElementWiseOperation.Operation.Add:
                dataOut = dataOut + data[i]
            elif self.operation is ElementWiseOperation.Operation.Subtract:
                dataOut = dataOut - data[i]
            elif self.operation is ElementWiseOperation.Operation.Multiply:
                dataOut = dataOut * data[i]
            elif self.operation is ElementWiseOperation.Operation.Divide:
                dataOut = dataOut / data[i]
        self.write(0, dataOut)