import json
import ioiopype as ioio

from ..pattern.io_node import IONode
from ..pattern.o_stream import OStream
from ..pattern.i_stream import IStream
from ..pattern.stream_info import StreamInfo

'''TODO NOT FINISHED YET'''

class IOIOPype(IONode):
    def __init__(self, nodes, connections, inputs, outputs):
        super().__init__()
        


class IOIOPypeBuilder:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)

        nodes = {}
        for node_data in data['Nodes']:
            if node_data['name'] == 'DataGenerator':
                node = ioio.DataGenerator(**node_data)
            elif node_data['name'] == 'ButterworthFilter':
                node = ioio.ButterworthFilter(**node_data)
            nodes[node_data['id']] = node
'''
READ JSON FILE
PARSE FILE
INITIALIZE NODES
CONNECT NODES
IIOIOPYPELINE
'''