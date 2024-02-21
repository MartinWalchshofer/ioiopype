# IOIOpype
 IOIOpype is processing framework for realtime applications written in python. Data is propergated from one processing node to the other.

## 'InputNode'
Input nodes can get data from 'OutputNodes'. Data is delivered via 'InputStream'. They can process data but do not propagate data to any other nodes.

### Implementing a new 'InputNode'
Add a new class to the 'input_nodes' folder

```
from ..pattern.input_node import InputNode
from ..pattern.input_stream import InputStream

class InputClass(InputNode):
    def __init__(self):
        super().__init__() #call InputNode constructor
        self.add_input_stream(InputStream(0, 'in')) #define input streams 
        self.NodeUpdateMode = self.UpdateMode.Synchronized #define update mode"

    def __del__(self):
        super().__del__() #call InputNode destructor

    #update is called according to the 'NodeUpdateMode'
    #if 'UpdateMode.Synchronized' is defined update is called whenever all attached streams delivered data
    #if 'UpdateMode.Asynchron' is defined update is called whenever any attached stream delivered data
    def update(self):
        #read data from stream buffer
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             #DO SOMETHING

```

## Create 'requirements.txt'

Execute this command from root folder to create 'requirements.txt'.

```pipreqs ./ --force``` 