from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import json

class ToWorkspace(INode):
    def __init__(self):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'data', StreamInfo.Datatype.Variable)))
        self.__eventHandlers = []

    def __del__(self):
        super().__del__()

    def __dict__(self):
        return {
            "name": self.__class__.__name__,
        }
    
    def __str__(self):
        return json.dumps(self.__dict__())

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)

    def add_data_available_eventhandler(self, handler):
        self.__eventHandlers.append(handler)

    def remove_data_available_eventhandler(self, handler):
        self.__eventHandlers.remove(handler)

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
            for handler in self.__eventHandlers:
                handler(data)