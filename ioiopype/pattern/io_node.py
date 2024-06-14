from .i_node import INode
from .o_node import ONode

class IONode(INode, ONode):
    def __init__(self):
        super().__init__()
        super(INode, self).__init__()

    def __del__(self):
        super().__del__()
        super(INode, self).__del__()