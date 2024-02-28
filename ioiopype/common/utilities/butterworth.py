
from scipy.signal import butter
from enum import Enum

class FilterType(Enum):
        Lowpass = 1
        Highpass = 2
        Bandpass = 3
        Notch = 4

def butterworth(type, samplingRate, order, cutoffFrequencies):
    b = 0
    a = 0
    if type is FilterType.Lowpass or type is FilterType.Highpass:
        if len(cutoffFrequencies) != 1:
            raise ValueError("Number of cutoff frequencies must be 1 for high and lowpass filters.")
    if type is FilterType.Bandpass or type is FilterType.Notch:
        if len(cutoffFrequencies) != 2:
            raise ValueError("Number of cutoff frequencies must be 2 for bandpass and notch filters.")
    if type is FilterType.Lowpass:
        b, a = butter(order, cutoffFrequencies[0]/(samplingRate/2), 'lowpass', analog=False)
    elif type is FilterType.Highpass:
        b, a = butter(order, cutoffFrequencies[0]/(samplingRate/2),'highpass', analog=False)
    elif type is FilterType.Bandpass:
        b, a = butter(order, [cutoffFrequencies[0]/(samplingRate/2),cutoffFrequencies[1]/(samplingRate/2)],'bandpass', analog=False)
    elif type is FilterType.Notch:
        b, a = butter(order, [cutoffFrequencies[0]/(samplingRate/2),cutoffFrequencies[1]/(samplingRate/2)],'bandstop', analog=False)
    else:
        raise TypeError("Unknown type")
    return b, a 