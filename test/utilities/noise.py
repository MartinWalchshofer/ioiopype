
import numpy as np

def pinknoise_multichannel(num_samples, num_channels):
    pink_noise_matrix = np.zeros((num_samples, num_channels))
    for i in range(num_channels):
        pink_noise_matrix[:, i] = pinknoise(num_samples)
    return pink_noise_matrix

def pinknoise(num_samples):
    white_noise = np.random.randn(num_samples)
    fft_white_noise = np.fft.fft(white_noise)
    freqs = np.fft.fftfreq(num_samples)
    pink_spectrum = np.sqrt(np.abs(freqs))
    fft_pink_noise = fft_white_noise * pink_spectrum
    pink_noise = np.fft.ifft(fft_pink_noise)
    pink_noise /= np.std(pink_noise)
    return pink_noise.real