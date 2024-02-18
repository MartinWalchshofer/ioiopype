from ..pattern.input_node import InputNode
from ..pattern.input_stream import InputStream

class ConsoleLog(InputNode):
    def __init__(self):
        super().__init__()
        self.add_stream(InputStream(0, 'in'))

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             print(data)