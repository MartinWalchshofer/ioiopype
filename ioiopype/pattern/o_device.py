#Copyright © 2024 Martin Walchshofer

from .o_node import ONode
from abc import ABC, abstractmethod

class ODevice( ONode):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    @staticmethod
    @abstractmethod
    def start_scanning(self):
        pass

    @staticmethod
    @abstractmethod
    def stop_scanning(self):
        pass

    @staticmethod
    @abstractmethod
    def add_devices_discovered_eventhandler(handler):
        pass

    @staticmethod
    @abstractmethod
    def remove_devices_discovered_eventhandler():
        pass