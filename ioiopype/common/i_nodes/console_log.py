from ...pattern.i_node import INode
from ...pattern.i_stream import IStream

class ConsoleLog(INode):
    def __init__(self):
        super().__init__()
        self.add_i_stream(IStream(0, 'in'))

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             print("{0}\n".format(data))