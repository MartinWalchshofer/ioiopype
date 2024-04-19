from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import numpy as np
import json
from json import JSONEncoder
from enum import Enum

class Serialize(IONode):
    class Mode(Enum):
        Json = 1
        xml = 2

    class __NumpyArrayEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    def __init__(self, tag, mode):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.String)))    
        self.__id = tag
        self.__mode = mode
        
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
            "id": self.__id,
            "mode": self.__mode.name,
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
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            if data.ndim == 1:
                data = np.array([data])
            if data.ndim > 2:
                raise ValueError("Dimensions do not fit")
            if self.__mode is Serialize.Mode.Json:
                self.write(0, json.dumps({self.__id: data}, cls=self.__NumpyArrayEncoder))
            elif self.__mode is Serialize.Mode.xml:
                raise NotImplementedError("Not implemented yet")
            else:
                raise TypeError("Unknown type")