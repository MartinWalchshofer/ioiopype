from enum import Enum

class StreamInfo:
    class Datatype(Enum):
        Sample = 1,
        Frame = 1,
        Variable = 1,

    def __init__(self, id : int, name :str, type : Datatype):
        self.Id : int = id
        self.Name : str = name
        self.Type = type
