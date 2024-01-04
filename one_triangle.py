import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

S21_freq = []


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    index_path = os.path.join(base_path, 'data', 'get_triangle')
    
    index_dict = {}
    
    for root, dirs, files in os.walk(index_path):
        for file in files:
            
            if '.csv' in file:
                
                label = file.split('.')[0] + 'cm'
                df = pd.read_csv(os.path.join(root, file))
                
                index_dict[label] = df['Frequency']
                
    
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            
            if 'S2P' in file and file.split('.')[0].isdigit():
                        
                label = file.split('.')[0] + 'cm'
                
                if label in index_dict.keys():
                
                    df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                    
                    frequency = df['Frequency'].values
                    phase = df['S21_phase'].values
                    
                    index_left = frequency.tolist().index(index_dict[label][0])
                    index_right = frequency.tolist().index(index_dict[label][1])  
                    
                    frequency = frequency[index_left:index_right]
                    phase = phase[index_left:index_right]
                    
                    plt.plot(frequency, phase, label=label)
                    plt.ylabel('Phase (deg)')
                    plt.xlabel('Frequency (GHz)')
                    plt.title('Frequency vs. Phase {}'.format(label))
                    plt.legend()
                    plt.show()
                
                
                        
                    
                         
                
                