from ..pattern.output_node import OutputNode
from ..pattern.output_stream import OutputStream
from ..pattern.input_node import InputNode
from ..pattern.input_stream import InputStream
from ..utilities.overriding_buffer import OverridingBuffer

class Framer(InputNode, OutputNode):
    def __init__(self):
        super().__init__()
        super(InputNode, self).__init__()
        self.add_input_stream(InputStream(0, 'sample'))
        self.add_input_stream(InputStream(1, 'trigger'))
        self.add_output_stream(OutputStream(0,'frame'))
        #TBD

    def __del__(self):
        super().__del__()
        super(InputNode, self).__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             x=0 #tbd  