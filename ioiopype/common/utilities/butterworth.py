
from scipy.signal import butter
from .filter_types import FilterType

def butterworth(type, samplingRate, order, cutoffFrequencies):
    b = 0
    a = 0
    if type is FilterType.Lowpass or type is FilterType.Highpass or type == FilterType.Lowpass.name or type == FilterType.Highpass.name:
        if len(cutoffFrequencies) != 1:
            raise ValueError("Number of cutoff frequencies must be 1 for high and lowpass filters.")
    if type is FilterType.Bandpass or type is FilterType.Notch or type == FilterType.Bandpass.name or type == FilterType.Notch.name:
        if len(cutoffFrequencies) != 2:
            raise ValueError("Number of cutoff frequencies must be 2 for bandpass and notch filters.")
    if type is FilterType.Lowpass or type == FilterType.Lowpass.name:
        b, a = butter(order, cutoffFrequencies[0]/(samplingRate/2), 'lowpass', analog=False)
    elif type is FilterType.Highpass or type == FilterType.Highpass.name:
        b, a = butter(order, cutoffFrequencies[0]/(samplingRate/2),'highpass', analog=False)
    elif type is FilterType.Bandpass or type == FilterType.Bandpass.name:
        b, a = butter(order, [cutoffFrequencies[0]/(samplingRate/2),cutoffFrequencies[1]/(samplingRate/2)],'bandpass', analog=False)
    elif type is FilterType.Notch or type == FilterType.Notch.name:
        b, a = butter(order, [cutoffFrequencies[0]/(samplingRate/2),cutoffFrequencies[1]/(samplingRate/2)],'bandstop', analog=False)
    else:
        raise TypeError("Unknown type")
    return b, a 