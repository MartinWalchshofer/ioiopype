from ..pattern.input_node import InputNode
from ..pattern.input_stream import InputStream

class ConsoleLog(InputNode):
    def __init__(self):
        super().__init__()
        self.add_stream(InputStream(0, 'in'))

    def update(self):
        self.InputStreams