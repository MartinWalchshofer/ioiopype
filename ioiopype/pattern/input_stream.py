#Copyright © 2024 Martin Walchshofer

import queue

class InputStream:
    def __init__(self, id : int, name : str):
        self.__queue : queue.Queue = queue.Queue()
        self.DataCount : int = 0
        self.Id : int = id
        self.Name : str = name
        self.IsConnected = False
        self.__eventHandlers : function = []
    
    def write(self, data):
        self.__queue.put(data)
        self.DataCount = self.__queue.qsize()
        for handler in self.__eventHandlers:
            handler() 

    def read(self):
        if self.__queue.qsize() > 0:
            try:
                return self.__queue.get()
            except:
                return None
        else:
            return None 

    def add_data_available_eventhandler(self, handler):
        self.__eventHandlers.append(handler)

    def remove_data_available_eventhandler(self, handler):
        self.__eventHandlers.remove(handler)