import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.signal


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    signal_path = os.path.join(base_path, 'signal', 'signal.xlsx')
    peak_path = os.path.join(base_path, 'signal', 'two_peaks_manual_record.csv')
    
    signal_df = pd.read_excel(signal_path)
    t = signal_df['t'].values
    
    peak = pd.read_csv(peak_path)
    
    distance_df = pd.DataFrame()
    
    for i in range(len(peak.columns)):
        
        peaks = peak.iloc[:, i].values
        t_diff = t[peak.iloc[1, i]] - t[peak.iloc[0, i]]
        distance = t_diff * 3e8 / 2 * 100
        
        distance_df[peak.columns[i]] = [peak.columns[i], distance]
        
    print(distance_df)