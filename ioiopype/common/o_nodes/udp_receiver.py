#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ..utilities.realtime_clock import RealtimeClock
import numpy as np
import json
import socket
import threading
import time

class UDPReceiver(ONode):
    def __init__(self, ip, port):
        super().__init__()
        self.add_o_stream(OStream(StreamInfo(0, 'data', StreamInfo.Datatype.String)))
        self.__ip = ip
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.settimeout(0.1)
        self.__socket.bind((self.__ip, self.__port ))
        self.__buffersize = 1024
        self.__updateThreadRunning = False
        self.__updateThread = None
        self.__start()

    def __del__(self):
        self.__stop()
        self.__socket.close()
        super().__del__()

    def __dict__(self):
        ostreams = []
        for i in range(0,len(self.OutputStreams)):
            ostreams.append(self.OutputStreams[i].StreamInfo.__dict__())
        return {
            "name": self.__class__.__name__,
            "ip": self.__ip,
            "port": self.__port,
            "o_streams": ostreams
        }
    
    def __str__(self):
        return json.dumps(self.__dict__(), indent=4)

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)

    def __start(self):
        if not self.__updateThreadRunning:
            self.__updateThreadRunning = True
            self.__updateThread = threading.Thread(target=self.__updateThread_DoWork, daemon=True)
            self.__updateThread.start()
           
    def __stop(self):
        if self.__updateThreadRunning:
            self.__updateThreadRunning = False
            self.__updateThread.join()
            self.__updateThread = None

    def __updateThread_DoWork(self):
        while self.__updateThreadRunning:
            try:
                data = self.__socket.recv(self.__buffersize)
                if data is not None:
                    self.write(0, data.decode('utf-8'))
            except:
                time.sleep(0.1)