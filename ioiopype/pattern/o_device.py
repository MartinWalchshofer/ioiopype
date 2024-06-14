from .o_node import ONode
from abc import abstractmethod

class ODevice( ONode):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    @staticmethod
    @abstractmethod
    def start_scanning():
        pass

    @staticmethod
    @abstractmethod
    def stop_scanning():
        pass

    @staticmethod
    @abstractmethod
    def add_devices_discovered_eventhandler(handler):
        pass

    @staticmethod
    @abstractmethod
    def remove_devices_discovered_eventhandler():
        pass