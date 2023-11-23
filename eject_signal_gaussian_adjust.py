import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
from scipy.interpolate import interp1d
from sklearn.preprocessing import StandardScaler
import math
import os
from rich.progress import track

def normalize_spectrum(spectrum):
    # 计算数组的最大值和最小值
    max_value = np.max(spectrum)
    min_value = 0
    
    # 归一化处理
    normalized_spectrum = (spectrum - min_value) / (max_value - min_value)
    
    return normalized_spectrum


def gaussian_spcturm(f, fc, bw, bwr):
    
    ref = pow(10.0, bwr / 20.0)
    # fdel = fc*bw/2:  g(fdel) = ref --- solve this for a
    #
    # pi^2/a * fc^2 * bw^2 /4=-log(ref)
    a = -(math.pi * fc * bw) ** 2 / (4.0 * math.log(ref))
    
    spectrum = np.exp(- (math.pi ** 2) * (2 * math.pi * f ** 2) / a)

        
    spectrum_positive = np.exp(- (math.pi ** 2) * ((f - fc) ** 2) / a)
    spectrum_negative = np.exp(- (math.pi ** 2) * ((f + fc) ** 2) / a)
    spectrum_modu = spectrum_positive + spectrum_negative
    
    return spectrum, spectrum_modu



# Generate UWB signal parameters
sampling_rate = 10e13 # Sampling rate in Hz
duration = 1e-8 # Duration of the signal in seconds
amplitude = 1.0  # Amplitude of the UWB signal
start_frequency = 100e3
end_frequency = 6.5e9
center_frequency = (start_frequency + end_frequency) / 2  # Center frequency of the UWB signal
bandwidth =  (end_frequency - start_frequency) / center_frequency # Bandwidth of the UWB signal

# Generate time vector
t = np.linspace(-duration/2, duration/2, int(sampling_rate * duration))

# Generate UWB signal
# _, uwb_signal = signal.gausspulse(t, fc=center_frequency, bw=bandwidth, retenv=True)
uwb_signal = signal.gausspulse(t, fc=center_frequency, bw=bandwidth)

print(uwb_signal)

# Perform Fourier transform on the UWB signal
spectrum = np.fft.fft(uwb_signal)
frequencies = np.fft.fftfreq(len(uwb_signal), d=1/sampling_rate)
# spectrum = np.fft.fftshift(spectrum)
# frequencies = np.fft.fftshift(frequencies)


# Get amplitude and phase from the spectrum
amplitude_spectrum = np.abs(spectrum)
phase_spectrum = np.angle(spectrum)

# amplitude_spectrum = normalize_spectrum(amplitude_spectrum)

# Reconstruct UWB signal from amplitude and phase spectra
reconstructed_signal = np.fft.ifft(amplitude_spectrum * np.exp(1j * phase_spectrum))

sorted_indices = np.argsort(frequencies)

frequencies_sorted = frequencies[sorted_indices]
amplitude_spectrum_sorted = amplitude_spectrum[sorted_indices]
phase_spectrum_sorted = phase_spectrum[sorted_indices]


# zip = zip(frequencies, amplitude_spectrum, phase_spectrum)
# pd.DataFrame(zip).to_csv('test.csv')

# Plotting the results
plt.figure(figsize=(10, 6))

# Plot time-domain UWB signal
plt.subplot(2, 2, 1)
plt.plot(t, uwb_signal)
plt.title('UWB Signal (Time Domain)')
plt.xlabel('Time')
plt.ylabel('Amplitude')

# Plot frequency spectrum
plt.subplot(2, 2, 2)
plt.plot(frequencies_sorted, normalize_spectrum(amplitude_spectrum_sorted))
plt.title('Frequency Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')

# Plot phase spectrum
plt.subplot(2, 2, 3)
plt.plot(frequencies_sorted, phase_spectrum_sorted)
plt.title('Phase Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Phase')

# Plot reconstructed UWB signal
plt.subplot(2, 2, 4)
plt.plot(t, reconstructed_signal)
plt.title('Reconstructed UWB Signal (Time Domain)')
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

mask = abs(frequencies) < 7e9
frequencies_mask = frequencies[mask]
amplitude_spectrum_mask = amplitude_spectrum[mask]
phase_spectrum_mask = phase_spectrum[mask]

amplitude_spectrum_mask = normalize_spectrum(amplitude_spectrum_mask)

reconstructed_signal = np.fft.ifft(amplitude_spectrum_mask * np.exp(1j * phase_spectrum_mask))

sorted_indices = np.argsort(frequencies_mask)
frequencies_sorted = frequencies_mask[sorted_indices]
amplitude_spectrum_sorted = amplitude_spectrum_mask[sorted_indices]
phase_spectrum_sorted = phase_spectrum_mask[sorted_indices]



# spectrum_saved = pd.DataFrame(list(zip(frequencies_sorted, amplitude_spectrum_sorted, phase_spectrum_sorted)), columns=['freq', 'amp', 'phase'])
# pd.DataFrame(spectrum_saved).to_csv('./data/UWB_signal_gaussianPulse_freq_amp_pair.csv', index=False)


plt.figure(figsize=(10, 6))

# Plot time-domain UWB signal
plt.subplot(2, 2, 1)
plt.plot(t, uwb_signal)
plt.title('UWB Signal (Time Domain)')
plt.xlabel('Time')
plt.ylabel('Amplitude')

# Plot frequency spectrum
plt.subplot(2, 2, 2)
plt.plot(frequencies_sorted, amplitude_spectrum_sorted)
plt.axvline(x=start_frequency, color='r', linestyle='--')
plt.axvline(x=center_frequency, color='r', linestyle='--')
plt.axvline(x=end_frequency, color='r', linestyle='--')
plt.title('Frequency Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')

# Plot phase spectrum
plt.subplot(2, 2, 3)
plt.plot(frequencies_sorted, phase_spectrum_sorted)
plt.title('Phase Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Phase')

# Plot reconstructed UWB signal
plt.subplot(2, 2, 4)
plt.plot(np.linspace(-duration/2, duration/2, len(reconstructed_signal)), reconstructed_signal)
plt.title('Reconstructed UWB Signal (Time Domain)')
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()


plt.figure(figsize=(5, 8))

_, spectrum = gaussian_spcturm(frequencies_sorted, center_frequency, bandwidth, -6)

plt.subplot(3, 1, 1)
plt.plot(frequencies_sorted, spectrum)
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Gaussian Impluse Mag Spectrum')
plt.xlim(-7e9, 7e9)
plt.ylim(0, 1.1)
plt.axvline(x=start_frequency, color='r', linestyle='--')
plt.axvline(x=center_frequency, color='r', linestyle='--')
plt.axvline(x=end_frequency, color='r', linestyle='--')
plt.axhline(y=0.5, color='r', linestyle='--')



base_path = os.path.dirname(__file__)
eject_signal_df = pd.read_csv(os.path.join(base_path, 'data', 'exp01', '10cm', 'TOUCHSTONE.S2P'), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])

frequencies = eject_signal_df['Frequency'].values
phase_spectrum = [0] * len(frequencies)

plt.subplot(3, 1, 2)
plt.plot(frequencies, phase_spectrum)
plt.xlabel('Frequency')
plt.ylabel('Phase')
plt.title('Gaussian Impluse Phase Spectrum')

_, spectrum = gaussian_spcturm(frequencies, center_frequency, bandwidth, -6)

spectrum = normalize_spectrum(spectrum)

t = np.linspace(-duration/2, duration/2, int(1e5))

signal = np.zeros(len(t))

for i in track(range(len(frequencies)), description='Generating Gaussian Pulse...'):
    
    freq = frequencies[i]
    amp = spectrum[i]
    phase = phase_spectrum[i]
    
    component = amp * np.cos(2 * np.pi * freq * t + phase)
    signal += component
    
signal = signal / len(frequencies)
    
plt.subplot(3, 1, 3)
plt.plot(t, signal)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Gaussian Pulse')
plt.tight_layout()
plt.savefig(os.path.join(base_path, 'fig', 'eject_gaussian_pulse.png'))

spectrum_saved = pd.DataFrame(list(zip(frequencies, spectrum, phase_spectrum)), columns=['freq', 'amp', 'phase'])
spectrum_saved.to_csv(os.path.join(base_path, 'ref', 'eject_gaussian_pulse_freq_amp_pair.csv'), index=False)





