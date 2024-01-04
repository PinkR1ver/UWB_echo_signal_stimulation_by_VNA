import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rich.progress import track


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    save_path = os.path.join(base_path, 'data', 'ground_truth')
    
    labels = []
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            
            if 'S2P' in file and file.split('.')[0].isdigit():
                        
                label = file.split('.')[0] + 'cm'
                labels.append(label)
            
                df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequency = df['Frequency'].values
                phase = df['S21_phase'].values
                
                
                plt.figure(figsize=(12, 5))
                plt.plot(frequency, phase, label='Receive')
                plt.ylabel('Phase (deg)')
                
                ground_truth_phase = (-(float(label[:-2]) * (10 ** -2) * 2 * frequency / 3e8) * 360) % 360 - 180
                
                plt.plot(frequency, ground_truth_phase, label='Ground Truth')
                plt.xlabel('Frequency (GHz)')
                plt.title('Frequency vs. Phase {}'.format(label))
                plt.legend()
                plt.show()
                
                # save ground truth to .csv file
                df = pd.DataFrame({'Frequency': frequency, 'Phase': ground_truth_phase})
                df.to_csv(os.path.join(save_path, label + '.csv'), index=False)
                
