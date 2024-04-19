from enum import Enum
import json

class StreamInfo:
    class Datatype(Enum):
        Sample = 1,
        Frame = 2,
        String = 3,
        Any = 4,

    def __init__(self, id : int, name :str, type : Datatype):
        self.Id : int = id
        self.Name : str = name
        self.Type = type
    
    def __dict__(self):
        return {
            "id": self.Id,
            "name": self.Name,
            "type": self.Type.name,
        }
    
    def __str__(self):
        return json.dumps(self.__dict__(), indent=4)
    
    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        return cls(**ds)