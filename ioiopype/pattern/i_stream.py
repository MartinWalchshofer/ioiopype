#Copyright © 2024 Martin Walchshofer

import queue
from .stream_info  import StreamInfo

class IStream:
    def __init__(self, streamInfo : StreamInfo):
        self.__queue : queue.Queue = queue.Queue()
        self.DataCount : int = 0
        self.StreamInfo = streamInfo
        self.IsConnected = False
        self.__eventHandler : function
        self.__readCnt = 0
    
    def write(self, data):
        self.__queue.put(data)
        self.DataCount = self.__queue.qsize()
        if self.__eventHandler is not None:
            self.__eventHandler()

    def read(self):
        if self.__queue.qsize() > 0:
            try:
                self.__readCnt += 1
                return self.__queue.get()
            except:
                return None
        else:
            return None 

    def set_data_available_eventhandler(self, handler):
        self.__eventHandler = handler

    def remove_data_available_eventhandler(self, handler):
        self.__eventHandler = None