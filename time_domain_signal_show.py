import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.signal


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    signal_path = os.path.join(base_path, 'signal', 'signal.xlsx')
    signal_df = pd.read_excel(signal_path)
    
    mc_signal = signal_df['MC'].values
    t = signal_df['t'].values                                                                                                           
    
    for i in range(2, len(signal_df.columns)):
        
        signal = signal_df.iloc[:, i].values
        signal = signal - mc_signal
        
        # find the peak of the signal and plot out
        peaks, _ = scipy.signal.find_peaks(signal)
        print(peaks)
        plt.plot(t, signal)
        plt.plot(t[peaks], signal[peaks], "x")
        plt.xlabel('Time(s)')
        plt.ylabel('Magnitude')
        plt.title(f'{signal_df.columns[i]} Signal')
        plt.show()
        