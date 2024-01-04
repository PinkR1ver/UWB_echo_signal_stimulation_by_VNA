import numpy as np
import pandas as pd
import os
import random
import matplotlib.pyplot as plt
import scipy.signal
from rich.progress import track


def logmag2liner(x):
    return 10 ** (x/20)


base = ['05cm', '12cm', '20cm', '32cm']

if __name__ == '__main__':
    
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    
    labels = []
    flight_time = []
    
    t = np.linspace(0, 1e7, int(1e6))
    
    freq_index = 9234
    phase_list = []
    
    amp = 0.9
    
    for root, dirs, files in os.walk(data_path):
        for file in track(files, description='Processing...'):
            
            if "S2P" in file and file.split('.')[0].isdigit():
                
                
                label = file.split('.')[0] + 'cm'
                
                if label not in base:
                    continue
                
                labels.append(label)
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequency = s_df['Frequency'].values
                phase = s_df['S21_phase'].values
                amp = s_df['S21_amp'].values
                
                signal = np.zeros(len(t))
                
                for ph, am, freq in zip(phase, amp, frequency):
                    signal += am * np.cos(2 * np.pi * freq * t + ph)
                    
                plt.plot(t, signal, label=label)
                peaks = np.argmax(signal)
                plt.plot(t[peaks], signal[peaks], 'rx', label='Peaks')
                
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Receive Signal')
    plt.legend()
    plt.show()
                
                