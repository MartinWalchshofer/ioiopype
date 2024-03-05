from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo

class ToWorkspace(INode):
    def __init__(self):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Variable)))
        self.__eventHandlers = []

    def __del__(self):
        super().__del__()

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