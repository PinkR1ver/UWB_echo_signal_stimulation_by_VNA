import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import sympy as sp
from rich.progress import track
import math


def logmag2liner(x):
    return 10 ** (x/20)

if __name__ == '__main__':
    
    file_dir = os.path.dirname(__file__)
    data_path = os.path.join(file_dir, 'data', 'exp01')
    
    eject_signal_df = pd.read_csv(os.path.join(data_path, '10cm', 'TOUCHSTONE.S2P'), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
    
    duration = 1e-8 # Duration of the signal in seconds
    freqencies = eject_signal_df['Frequency'].to_numpy()
    amp_spectrum = np.vectorize(logmag2liner)(eject_signal_df['S11_amp'].to_numpy())
    phase_spectrum = eject_signal_df['S11_phase'].to_numpy()
    
    
    ref_df = pd.read_csv(os.path.join(file_dir, 'ref', 'eject_gaussian_pulse_freq_amp_pair.csv'), skiprows=1, names=['freq', 'amp', 'phase'])
    
    amp_ref = ref_df['amp'].to_numpy()
        
    amp_adjust = amp_spectrum * amp_ref
    
    t = np.linspace(0, 1e-8, int(1e5))
    
    signal = np.zeros(len(t))
    
    for i in track(range(len(freqencies)), description='Generating Gaussian Pulse...'):
        
        freq = freqencies[i]
        amp = amp_adjust[i]
        phase = phase_spectrum[i]
        
        component = amp * np.cos(2 * np.pi * freq * t + phase)
        
        signal += component
        
    plt.plot(t, signal)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.show()
    
        
        
        
    
    
    