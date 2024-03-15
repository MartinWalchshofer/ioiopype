# IOIOpype
 IOIOpype is processing framework for realtime applications written in python. Data is propergated between Nodes that can be connected via Streams. Nodes can be input nodes 'INode', output nodes 'ONode' or input and output nodes 'IONode'. Algorithms and signal processing pipelines can be prototyped easily by combining multiple nodes.

## Supported Devices
- Unicorn Hybrid Black (g.tec medical engineering GmbH)
- Unicorn Hybrid Black Simulator - TBD

## INodes
- ConsoleLog - Writes received data to the console
- ToWorkspace - Propagates data to the main thread via event
- FramePlot - Plots a data frame
-  SamplePlot - Plots time series data

## IONodes
- Buffer - Buffers data with a defined window size and overlap
- PWelch - Calculates a Pwelch spectrum from a frame
- Downsample - Samples a data frame down by a given factor
- OffsetCorrection - Removes the offset from a data frame
- ButterworthFilter - Applies a butterworth filter to a sample based signal
- ToSample - Slices and forwards a data frame into samples

## ONodes
- DataGenerator - Generates sample based time series data with configurable frequency and amplitude
- Frame - Allows to send a data frame to INodes

## Supported platforms

| Windows    | Linux    | Mac  |
| :--------- |:---------| :----|

## Create 'requirements.txt'

Execute this command from root folder to create 'requirements.txt'.

```pipreqs ./ --force``` 

## Contact
Support this project: [![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/MartinWalchshofer)<br>
Join IOIOPype on [Discord](https://discord.gg/pKEumyD9)<br>
Contact: ```mwalchsoferyt at gmail dot com```