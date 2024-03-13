#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
import json

class Frame(ONode):
    def __init__(self):
        super().__init__()
        self.add_o_stream(OStream(StreamInfo(0, 'data', StreamInfo.Datatype.Frame)))

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

    def send_frame(self, frame):
        self.write(0, frame)