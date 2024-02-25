import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# Generate a sample signal
fs = 1000  # Sampling frequency
t = np.linspace(0, 1, fs, endpoint=False)  # 1 second of signal
x = np.sin(2 * np.pi * 5 * t)*10  # Sinusoidal signal at 5 Hz

# Compute the power spectral density using pwelch
frequencies, psd = welch(x, fs=fs, scaling='spectrum', average='median')

# Compute the absolute amplitude spectrum
amplitude = np.sqrt(psd)

# Plot the amplitude spectrum
plt.figure()

plt.plot(frequencies, amplitude)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Absolute Amplitude Spectrum')
plt.grid(True)
plt.show()
input()