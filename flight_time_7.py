import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from rich.progress import track
from scipy.signal import hilbert

freq_range = [7990, 9400]


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    
    t = np.linspace(0, 2 * 1e-6, int(1 * 1e2))
    labels = []
    
    figure = plt.figure(figsize=(12, 60))
    
    for root, dirs, files in os.walk(data_path):
        for index, file in enumerate(files):
            
            if file.split('.')[0] != 'MC':
                continue
            else:
                
                df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
            
                freqency = df['Frequency'].values
                phase = df['S21_phase'].values
                amp = df['S21_amp'].values
                
                freqency = freqency[freq_range[0]:freq_range[1]]
                phase = phase[freq_range[0]:freq_range[1]]
                amp = amp[freq_range[0]:freq_range[1]]
                
                mc_signal = np.zeros(len(t))
                
                for freq, pha, am in track(zip(freqency, phase, amp), description='MC signal Processing...', total=len(freqency)):
                    mc_signal += am * np.cos(2 * np.pi * freq * t + pha)
                    
                break
                
    
    for root, dirs, files in os.walk(data_path):
        for index, file in enumerate(files):
            
            
            if file.split('.')[0].isdigit(): 
                label = file.split('.')[0] + 'cm'
                labels.append(label)
            else:
                continue
            
            df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
            
            freqency = df['Frequency'].values
            phase = df['S21_phase'].values
            amp = df['S21_amp'].values
            
            freqency = freqency[freq_range[0]:freq_range[1]]
            phase = phase[freq_range[0]:freq_range[1]]
            amp = amp[freq_range[0]:freq_range[1]]
            
            signal = np.zeros(len(t))
            
            for freq, pha, am in track(zip(freqency, phase, amp), description='{} Processing...'.format(label), total=len(freqency)):
                signal += am * np.cos(2 * np.pi * freq * t + pha)
            
            signal = signal - mc_signal
            
            analytic_signal = hilbert(signal)
            signal_envelope = np.abs(analytic_signal)
        
            plt.subplot(24, 1, index+1)
            plt.plot(t, signal_envelope, label=label)
            plt.ylabel('Amplitude (V)')
            plt.title('Time Domain Signal {}'.format(label))
            
            peak = np.argmax(signal_envelope)
            plt.plot(t[peak], signal_envelope[peak], 'rx', label='Peaks')
    
    plt.tight_layout()
    plt.xlabel('Time (s)')
    plt.savefig(os.path.join(base_path, 'fig', 'time_domain_signal_5.png'))
            