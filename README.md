# IOIOpype
 IOIOpype is processing framework for realtime applications written in python. Data is propergated from one processing node to the other.

## 'INode'
'INodes' can recevice data from 'ONodes' if they are connected. Data is delivered via a streams 'IStream'. They can process data but do not propagate data to any other nodes.

### Implementing a new 'INode'
Add a new class to the 'i_nodes' folder

```
from ..pattern.i_node import INode
from ..pattern.i_stream import IStream

class IClass(INode):
    def __init__(self):
        super().__init__() #call INode constructor
        self.add_i_stream(IStream(0, 'in')) #define istreams 
        self.NodeUpdateMode = self.UpdateMode.Synchronized #define update mode"

    def __del__(self):
        super().__del__() #call INode destructor

    #update is called according to the 'NodeUpdateMode'
    #if 'UpdateMode.Synchronized' is defined update is called whenever all attached streams delivered data
    #if 'UpdateMode.Asynchron' is defined update is called whenever any attached stream delivered data
    def update(self):
        #read data from stream buffer
        data = None
        if self.IStreams[0].DataCount > 0:
            data = self.IStreams[0].read()
        if data is not None:
             #DO SOMETHING

```

## Create 'requirements.txt'

Execute this command from root folder to create 'requirements.txt'.

```pipreqs ./ --force``` 