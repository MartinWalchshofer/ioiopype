import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import ioiopype as ioio
import numpy as np
import matplotlib.pyplot as mp

rowCount = 2500
columnCount = 8
mu = 100
sigma = 50
fs = 250

#create test data
data = mu + sigma * np.random.randn(rowCount, columnCount)

#define nodes
f = ioio.Frame()
ts = ioio.ToSample()
hp = ioio.ButterworthFilter(ioio.FilterType.Highpass, fs, 2, [1])
lp = ioio.ButterworthFilter(ioio.FilterType.Lowpass, fs, 2, [100])
n50 = ioio.ButterworthFilter(ioio.FilterType.Notch, fs, 2, [48,52])
b = ioio.Buffer(columnCount,rowCount,0)
tw = ioio.ToWorkspace()

#build pype
f.connect(0, ts.InputStreams[0])
ts.connect(0, hp.InputStreams[0])
hp.connect(0, lp.InputStreams[0])
lp.connect(0, n50.InputStreams[0])
n50.connect(0, b.InputStreams[0])
b.connect(0, tw.InputStreams[0])

#send data
f.send_frame(data)

#TBD
#wait until data is available

#plot timeseries
t = np.linspace(0, rowCount/fs, num=rowCount)
fig, axs = mp.subplots(columnCount, 1, sharex=True)
fig.subplots_adjust(hspace=0)
for i in range(columnCount):
    axs[i].plot(t, data[:, i], color='blue', linestyle='-')
    axs[i].set_ylabel(f'EEG {i+1} [µV]')
    axs[i].set_xlim(0, t[t.shape[0]-1])

axs[columnCount - 1].set_xlabel('t [s]')
mp.show()