#Copyright © 2024 Martin Walchshofer

from .input_stream import InputStream
import threading
from abc import ABC, abstractmethod
from enum import Enum

class InputNode(ABC):

    class UpdateMode(Enum):
        Synchronized = 1 #update when all input streams delivered data
        Asynchron = 2    #update when any input stream delivered data

    def __init__(self):
        self.InputStreams : list[InputStream] = []
        self.NodeUpdateMode = self.UpdateMode.Synchronized

        self.__event : threading.Event = threading.Event()
        self.__updateThreadRunning = False
        self.__updateThread = None
        self.__start()

    def __del__(self):
        self.__stop()

    def __start(self):
        if not self.__updateThreadRunning:
            self.__updateThreadRunning = True
            self.__updateThread = threading.Thread(target=self.__updateThread_DoWork, daemon=True)
            self.__updateThread.start()
           
    def __stop(self):
        if self.__updateThreadRunning:
            self.__updateThreadRunning = False
            self.__event.set()
            self.__updateThread.join()
            self.__updateThread = None

    def __on_data_available(self):
        if self.NodeUpdateMode is self.UpdateMode.Asynchron:
            self.__event.set()
        else:
            allStreamsAcquired = True
            for stream in self.InputStreams:
                if stream.DataCount <= 0:
                    allStreamsAcquired = False
                    break
            if allStreamsAcquired:
                self.__event.set()
        
    def __updateThread_DoWork(self):
        try:
            while self.__updateThreadRunning:
                self.__event.wait()
                self.__event.clear()
                if self.__updateThreadRunning:
                    self.update()
        except Exception as e:
            self.__stop()
        
    def add_stream(self, inputStream : InputStream):
        #TODO CHECK IF ID IS UNIQE
        if isinstance(inputStream, InputStream):
            self.InputStreams.append(inputStream)
            inputStream.add_data_available_eventhandler(self.__on_data_available)
        else:
            raise TypeError("'inputStream' must be type of 'InputStream'")

    @abstractmethod
    def update(self):
        pass
        
