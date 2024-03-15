'''
This test creates a pink noise frame with specified number of channels and samples.
The frame is processed sample by sample and ran throug some iir filters sequentially.
Data before and after filtering is plotted to verify that the desired frequency bands are dampened.
'''

import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import time
import ioiopype as ioio
import numpy as np
import matplotlib.pyplot as mp
import scipy.signal as sp
from utilities.noise import pinknoise_multichannel

def on_data_available(data):
    global dataProcessed
    dataProcessed = data

dataProcessed = None
rowCount = 2500
columnCount = 8
fs = 250
fclp = [10]
fchp = [80]
fcn = [48,52]

# create test data
data  = pinknoise_multichannel(rowCount, columnCount) * 100

#define nodes
f = ioio.Frame()
ts = ioio.ToSample()
hp = ioio.ButterworthFilter(ioio.FilterType.Highpass, fs, 2, fclp)
lp = ioio.ButterworthFilter(ioio.FilterType.Lowpass, fs, 4, fchp)
n50 = ioio.ButterworthFilter(ioio.FilterType.Notch, fs, 4, fcn)
b = ioio.Buffer(columnCount,rowCount,0)
tw = ioio.ToWorkspace()
tw.add_data_available_eventhandler(on_data_available)

#build pype
f.connect(0, ts.InputStreams[0])
ts.connect(0, hp.InputStreams[0])
hp.connect(0, lp.InputStreams[0])
lp.connect(0, n50.InputStreams[0])
n50.connect(0, b.InputStreams[0])
b.connect(0, tw.InputStreams[0])

#send data
f.send_frame(data)

#wait until data is processed
while dataProcessed is None:
    time.sleep(1)

tw.remove_data_available_eventhandler(on_data_available)

#plot timeseries
t = np.linspace(0, rowCount/fs, num=rowCount)
fig, axs = mp.subplots(columnCount, 1, sharex=True)
fig.subplots_adjust(hspace=0)
for i in range(columnCount):
    axs[i].plot(t, data[:, i], color='blue', linestyle='-')
    axs[i].plot(t, dataProcessed[:, i], color='red', linestyle='-')
    axs[i].set_ylabel(f'Ch. {i+1}')
    axs[i].set_xlim(0, t[t.shape[0]-1])
axs[columnCount - 1].set_xlabel('t [s]')
mp.show()

segmentLength = 5 * fs
frequencies, spectrum = sp.welch(data, fs=fs, nperseg=segmentLength, average='median', scaling='spectrum', axis=0)
frequenciesProcessed, spectrumProcessed = sp.welch(dataProcessed, fs=fs, nperseg=segmentLength, average='median', scaling='spectrum', axis=0)

fig, axs = mp.subplots(columnCount, 1, sharex=True)
fig.subplots_adjust(hspace=0)
for i in range(columnCount):
    axs[i].semilogy(frequencies, spectrum[:, i], color='blue', linestyle='-')
    axs[i].semilogy(frequenciesProcessed, spectrumProcessed[:, i], color='red', linestyle='-')
    axs[i].grid(True, which="both",ls="--",c='gray')
    axs[i].set_ylabel(f'Ch. {i+1}')
    axs[i].set_xlim(0, frequencies[frequencies.shape[0]-1])

axs[columnCount - 1].set_xlabel('frequency [Hz]')
mp.show()