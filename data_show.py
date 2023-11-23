import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def logmag2liner(x):
    return 10 ** (x/20)


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp02')
    
    labels = []
    S21_amp_spectrum = []
    S11_amp_spectrum = []
    S21_phase_spectrum = []
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if 'S2P' in file:
                
                df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequencies = df['Frequency'].values
                S21_amp = df['S21_amp'].values    
                S11_amp = df['S11_amp'].values    
                label = file.split('.')[0]
                
                if label.isdigit():
                    label = label + 'cm'
                labels.append(label)
                
                S21_amp_spectrum.append(S21_amp)
                S11_amp_spectrum.append(S11_amp)
                


    plt.figure(figsize=(5, 10))
    
    for amp_spectrum_S21, amp_spectrum_S11, label in zip(S21_amp_spectrum, S11_amp_spectrum, labels):
        plt.subplot(4, 1, 1)
        plt.plot(frequencies, amp_spectrum_S21, label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude(dB)')
        plt.title('S21 Magnitude Log Scale')
        plt.legend()
        
        plt.subplot(4, 1, 2)
        plt.plot(frequencies, np.vectorize(logmag2liner)(amp_spectrum_S21), label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.title('S21 Magnitude Linear')
        plt.legend()
        
        plt.subplot(4, 1, 3)
        plt.plot(frequencies, amp_spectrum_S11, label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude(dB)')
        plt.title('S11 Magnitude Log Scale')
        plt.legend()
        
        plt.subplot(4, 1, 4)
        plt.plot(frequencies, np.vectorize(logmag2liner)(amp_spectrum_S11), label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.title('S11 Magnitude Linear')
        plt.legend()
        
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(10, 8))
    
    for i in range(len(S21_amp_spectrum) - 1):
        
        S21_init = np.vectorize(logmag2liner)(S21_amp_spectrum[-1])
        S21 = np.vectorize(logmag2liner)(S21_amp_spectrum[i])
        
        S21 = S21 - S21_init
        
        # S21[S21 <= 0] = 0
        
        plt.plot(frequencies, S21, label=labels[i])
    
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.title('S21 Magnitude Linear')
    plt.legend()
    plt.show()
    
    AUC_list = []
    
    for i in range(len(S21_amp_spectrum) - 1):
        
        S21_init = np.vectorize(logmag2liner)(S21_amp_spectrum[-1])
        S21 = np.vectorize(logmag2liner)(S21_amp_spectrum[i])
        
        S21 = S21 - S21_init
        
        AUC = np.trapz(S21, frequencies)
        AUC_list.append(AUC)
        
    # plot AUC bar plot
    plt.figure(figsize=(10, 8))
    plt.bar(labels[:-1], AUC_list)
    plt.xlabel('Distance(cm)')
    plt.ylabel('AUC')
    plt.title('AUC vs Distance')
    plt.show()
    
    
    
    
    
        
    
    