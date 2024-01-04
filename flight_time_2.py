import numpy as np
import pandas as pd
import os
import random
import matplotlib.pyplot as plt
import scipy.signal


def logmag2liner(x):
    return 10 ** (x/20)

if __name__ == '__main__':
    
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    
    labels = []
    flight_time = []
    
    t = np.linspace(0, 1e-9, int(1e6))
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            
            if "S2P" in file and file.split('.')[0].isdigit():
                
                
                label = file.split('.')[0] + 'cm'
                labels.append(label)
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequency = s_df['Frequency'].values
                phase = s_df['S21_phase'].values
                
                flight_time = phase[30:] / (2 * np.pi)  * (1 / frequency[30:])
                ground_truth = float(label[:-2]) * 2 / 3e8
                
                plt.plot(frequency[30:], flight_time)
                plt.axhline(y=ground_truth, color='r', linestyle='-', label='Ground Truth')
                plt.text(0.8 * frequency[-1], ground_truth + 0.1e-9, f'{ground_truth:.3e}')
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Flight Time (s)')
                plt.title('Flight Time vs Frequency {}'.format(label))
                plt.show()
                