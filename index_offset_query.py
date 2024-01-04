import os
import pandas as pd
import numpy as np


if __name__ == '__main__':
    
    base_path = os.path.dirname(os.path.realpath(__file__))
    ref_path = os.path.join(base_path, 'data', 'exp06', '05.S2P')
    
    df = pd.read_csv(ref_path, skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
    frequency = df['Frequency'].values
    frequency = frequency.tolist()

    
    while True:
        
        # get input frequency
        freq1 = input('Frequency Left: ')
        freq2 = input('Frequency right: ')
        
        freq1_index = frequency.index(float(freq1))
        freq2_index = frequency.index(float(freq2))
        
        print(freq2_index - freq1_index)