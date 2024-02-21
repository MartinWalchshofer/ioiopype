from ..pattern.o_node import ONode
from ..pattern.o_stream import OStream
from ..pattern.i_node import INode
from ..pattern.i_stream import IStream
from ..utilities.overriding_buffer import OverridingBuffer

class Framer(INode, ONode):
    def __init__(self):
        super().__init__()
        super(INode, self).__init__()
        self.add_i_stream(IStream(0, 'sample'))
        self.add_i_stream(IStream(1, 'trigger'))
        self.add_o_stream(OStream(0,'frame'))
        #TBD

    def __del__(self):
        super().__del__()
        super(INode, self).__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             x=0 #tbd  