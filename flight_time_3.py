import numpy as np
import pandas as pd
import os
import random
import matplotlib.pyplot as plt
import scipy.signal


def logmag2liner(x):
    return 10 ** (x/20)


base = ['MCcm', '05cm', '12cm', '20cm', '32cm']

if __name__ == '__main__':
    
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    
    labels = []
    flight_time = []
    
    t = np.linspace(0, 1e-7, int(1e6))
    
    freq_index = 30
    phase_list = []
    
    amp = 0.9
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            
            if "S2P" in file:
                
                
                label = file.split('.')[0] + 'cm'
                
                if label not in base:
                    continue
                
                labels.append(label)
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequency = s_df['Frequency'].values
                phase = s_df['S21_phase'].values
                
                phase_list.append(phase[freq_index])
                frequency = frequency[freq_index]
                
    
    plt.plot(t, np.cos(2 * np.pi * frequency * t), label='Eject Signal')
    peaks = scipy.signal.find_peaks(np.cos(2 * np.pi * frequency * t), height=0)[0]
    plt.plot(t[peaks], np.cos(2 * np.pi * frequency * t)[peaks], 'rx', label='Peaks')
    
    for index, phase in enumerate(phase_list):
        
        signal = amp * np.cos(2 * np.pi * frequency * t + phase)
        amp -= 0.1
        plt.plot(t, signal, label=labels[index])
        
        peaks = scipy.signal.find_peaks(signal, height=0)[0]
        plt.plot(t[peaks], signal[peaks], 'rx', label='Peaks')
        
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Receive Signal at {} GHz'.format(frequency / 1e9))
    plt.legend()
    plt.show()
                
                