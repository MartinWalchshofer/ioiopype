
from ...pattern.i_node import INode
from ...pattern.i_stream import IStream
from ...pattern.stream_info import StreamInfo
import socket
import json

class UDPSender(INode):
    def __init__(self, ip, port):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'data', StreamInfo.Datatype.String)))
        self.__ip = ip
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self):
        self.__socket.close()
        super().__del__()

    def __dict__(self):
        istreams = []
        for i in range(0,len(self.InputStreams)):
            istreams.append(self.InputStreams[i].StreamInfo.__dict__())
        return {
            "name": self.__class__.__name__,
            "ip": self.__ip,
            "port": self.__port,
            "i_streams": istreams,
        }
    
    def __str__(self):
        return json.dumps(self.__dict__(), indent=4)

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)
        
    def update(self):
        for i in range (0, len(self.InputStreams)):
            data = self.InputStreams[i].read()
            self.__socket.sendto(data.encode('utf-8'), (self.__ip, self.__port))