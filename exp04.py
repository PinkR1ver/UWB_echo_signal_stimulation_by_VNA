import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from rich.progress import track

def logmag2liner(x):
    return 10 ** (x/20)


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp04')
    
    signal_df = pd.DataFrame(columns=['time', 'mutual_coupling_signal', '05cm', '10cm', '15cm', '20cm', '25cm'])
    
    ## ---- Part 1. Show the mutual coupling signal ----
    
    mutual_coupling_signal_S = pd.read_csv(os.path.join(data_path, 'mutual_coupling.S2P'), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
    
    freqency = mutual_coupling_signal_S['Frequency'].values
    phase = mutual_coupling_signal_S['S21_phase'].values
    S21_amp = mutual_coupling_signal_S['S21_amp'].values
    
    mutual_amp = np.vectorize(logmag2liner)(S21_amp)
    mutual_phase = phase
    
    plt.figure(figsize=(8, 5))
    
    plt.plot(freqency , np.vectorize(logmag2liner)(S21_amp))
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.title('S21 Magnitude Linear')
    plt.show()
    
    gaussian_factor = pd.read_csv(os.path.join(base_path, 'ref', 'eject_gaussian_pulse_freq_amp_pair.csv'), skiprows=1, names=['freq', 'amp', 'phase'])
    gaussian_factor = gaussian_factor['amp'].values
    
    # plot signal
    
    
    t = np.linspace(0, 1e-5, int(1e6)) 

    signal_df['time'] = t
    
    plt.figure(figsize=(8, 5))
    mutual_coupling_signal = np.zeros(len(t))

    for freq, gaussian_amp, amp, ph in track(zip(freqency, gaussian_factor, S21_amp, phase), description='Generating Received Signal...', total=len(freqency)):
        
        mutual_coupling_signal += gaussian_amp * amp * np.cos(2 * np.pi * freq * t + ph)
        
    mutual_coupling_signal = mutual_coupling_signal / len(freqency)
    
    signal_df['mutual_coupling_signal'] = mutual_coupling_signal
        
    plt.plot(t, mutual_coupling_signal)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.show()
    
    ## --- Part 2. Show the S21 data ---
    
    labels = []
    
    plt.figure(figsize=(8, 5))
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            
            if 'S2P' in file and file.split('.')[0].isdigit():
                
                label = file.split('.')[0] + 'cm'
                labels.append(label)
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                freqency = s_df['Frequency'].values
                phase = s_df['S21_phase'].values
                S21_amp = s_df['S21_amp'].values
                
                plt.plot(freqency , np.vectorize(logmag2liner)(S21_amp), label=label)
        
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.title('S21 Magnitude Linear')
    plt.legend()
    plt.show()
    
    labels = []
    
    plt.figure(figsize=(8, 5))
    
        
    for root, dirs, files in os.walk(data_path):
        for file in files:
            
            if 'S2P' in file and file.split('.')[0].isdigit():
                
                label = file.split('.')[0] + 'cm'
                labels.append(label)
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                freqency = s_df['Frequency'].values
                phase = s_df['S21_phase'].values
                S21_amp = s_df['S21_amp'].values
                
                signal = np.zeros(len(t))
                
                for freq, gaussian_amp, amp, ph in track(zip(freqency, gaussian_factor, S21_amp, phase), description='Generating Received Signal for {}...'.format(label), total=len(freqency)):
                    
                    signal += gaussian_amp * amp * np.cos(2 * np.pi * freq * t + ph)
                    
                signal = signal / len(freqency)
                
                signal = signal - mutual_coupling_signal
                
                signal_df[label] = signal
                
                plt.plot(t, signal, label=label)
                
        
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.title('Received Signal')
    plt.legend()
    plt.show()
    
    signal_df.to_csv(os.path.join(data_path, 'signal.csv'), index=False)