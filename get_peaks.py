import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'signal')
    
    peaks_list = []
    
    # Signal of Interest
    soi_list = ['40.txt', '45.txt', '50.txt', '55.txt', '60.txt', '65.txt', '70.txt', '75.txt', '80.txt', '85.txt', '90.txt', '95.txt']
    
    # read t from txt file
    t = np.loadtxt(os.path.join(data_path, 't.txt'))
    mc_signal = np.loadtxt(os.path.join(data_path, 'MC.txt'))
    
    figure, ax = plt.subplots()
    ax.plot(t, mc_signal)
    
    for soi in soi_list:
        
        # read numpy array from txt file
        signal = np.loadtxt(os.path.join(data_path, soi))
        
        # find peaks in [0.4 * 1e-8 - 0.8 * 1e-8], height in [0.005, 0.01]
        peaks, _ = scipy.signal.find_peaks(signal, height=(0.0055, 0.02))
        peaks = peaks[(t[peaks] > 0.4 * 1e-8) & (t[peaks] < 0.8 * 1e-8)]
        peaks_list.append(t[peaks][0])
        
        ax.plot(t, signal)
        ax.plot(t[peaks[0]], signal[peaks[0]], "x")
    
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Magnitude')
    ax.set_title('Signal')
    plt.show()
    
    t0_list = []
    
    for i in range(len(peaks_list)):
        t2 = peaks_list[i]
        t1 = int(soi_list[i].split('.')[0]) * 1e-2 * 2 / 3e8
        t0 = t2 - t1
        t0_list.append(t0)
        
    t0 = np.mean(t0_list)
    print(f't0: {t0:.2e}s')
    
    offset_list = []
    
    for i in range(len(peaks_list)):
        print(f'{soi_list[i].split('.')[0]} cm: {(peaks_list[i] - t0) * 3e8 / 2 * 100:.2f} cm')
        offset = (int(soi_list[i].split('.')[0]) - (peaks_list[i] - t0) * 3e8 / 2 * 100) / int(soi_list[i].split('.')[0])
        offset_list.append(offset)
        
    print(f'Offset: {(np.mean(offset_list) * 100):.2f}%')
    
        
    
        
        
        
        