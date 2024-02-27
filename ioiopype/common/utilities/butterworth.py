
from scipy.signal import butter
from ..enumerations.FilterType import FilterType

class Butterworth():    
    def __init__(self, type, samplingRate, order, cutoffFrequencies):
        if type is FilterType.Lowpass or type is FilterType.Highpass:
            if len(cutoffFrequencies) != 1:
                raise ValueError("Number of cutoff frequencies must be 1 for high and lowpass filters.")
        if type is FilterType.Bandpass or type is FilterType.Notch:
            if len(cutoffFrequencies) != 2:
                raise ValueError("Number of cutoff frequencies must be 2 for bandpass and notch filters.")
        if type is FilterType.Lowpass:
            self.b, self.a = butter(order, cutoffFrequencies[0]/(samplingRate/2), 'lowpass', analog=False)
        elif type is FilterType.Highpass:
            self.b, self.a = butter(order, cutoffFrequencies[0]/(samplingRate/2),'highpass', analog=False)
        elif type is FilterType.Bandpass:
            self.b, self.a = butter(order, [cutoffFrequencies[0]/(samplingRate/2),cutoffFrequencies[1]/(samplingRate/2)],'bandpass', analog=False)
        elif type is FilterType.Notch:
            self.b, self.a = butter(order, [cutoffFrequencies[0]/(samplingRate/2),cutoffFrequencies[1]/(samplingRate/2)],'bandstop', analog=False)
        else:
            raise TypeError("Unknown type")
    
    def get_coefficients(self):
        return self.b, self.a 