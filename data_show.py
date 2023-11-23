import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from rich.progress import track


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
        
        files.sort()
        
        for file in files:
            if 'S2P' in file:
                
                df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequencies = df['Frequency'].values
                S21_amp = df['S21_amp'].values    
                S11_amp = df['S11_amp'].values
                S21_phase = df['S21_phase'].values
                label = file.split('.')[0]
                
                if label.isdigit():
                    label = label + 'cm'
                labels.append(label)
                
                S21_amp_spectrum.append(S21_amp)
                S11_amp_spectrum.append(S11_amp)
                S21_phase_spectrum.append(S21_phase)
                    


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
    
    ref_df = pd.read_csv(os.path.join(base_path, 'ref', 'eject_gaussian_pulse_freq_amp_pair.csv'), skiprows=1, names=['freq', 'amp', 'phase'])
    
    amp_ref = ref_df['amp'].values
        
    t = np.linspace(0, 1e-5, int(1e6))
    
    signal = np.zeros(len(t))
    
    plt.figure(figsize=(10, 20))
    
    index = 1
    y_max = -np.inf
    y_min = np.inf

    for amp_spectrum_S21, amp_phase_S21, label in zip(S21_amp_spectrum, S21_phase_spectrum, labels):
        
        signal = np.zeros(len(t))
        
        amp_spectrum_S21 = np.vectorize(logmag2liner)(amp_phase_S21)
        amp_spectrum_S21 = amp_spectrum_S21 * amp_ref
        amp_spectrum_S21 = amp_spectrum_S21 - (S21_init * amp_ref)
        
        for amp, phase, freq in track(zip(amp_spectrum_S21, amp_phase_S21, frequencies), description='generating receving signal for {}...'.format(label), total=len(amp_spectrum_S21)):
            component = amp * np.cos(2 * np.pi * freq * t + phase)
            
            signal += component
        
        plt.subplot(9, 1, index)  
        index += 1
        
        y_max = max(np.max(signal / len(frequencies)), y_max)
        y_min = min(np.min(signal / len(frequencies)), y_min)
        
        plt.plot(t, signal / len(frequencies), label=label)
        plt.title('Receiving signal for distance {}'.format(label))
        plt.legend()
        plt.ylabel('Magnitude')
    
    plt.xlabel('Time (s)')
    plt.tight_layout()
    
    for i in range(1, 10):
        plt.subplot(9, 1, i)
        plt.ylim(y_min * 1.05, y_max * 1.05)
    
    plt.show()
            
        
        

    
    
    
    
        
    
    