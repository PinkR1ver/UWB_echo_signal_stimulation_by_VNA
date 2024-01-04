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
                S21_amp = s_df['S21_amp'].values
                
                random_index = random.randint(0, len(frequency) - 1)
                random_index = -30
                
                eject_signal = np.cos(2 * np.pi * frequency[random_index] * t)
                receive_signal  = logmag2liner(S21_amp[random_index]) * np.cos(2 * np.pi * frequency[random_index] * t + phase[random_index])
                
                rc_peaks, _ = scipy.signal.find_peaks(receive_signal, height=0)
                ej_peaks, _ = scipy.signal.find_peaks(eject_signal, height=0)
                
                if abs(rc_peaks[0] - ej_peaks[0]) > abs(rc_peaks[1] - ej_peaks[0]):
                    key_peak = 1
                else:
                    key_peak = 0
                             
                
                plt.figure(figsize=(8, 5))
                plt.plot(t, eject_signal, label='Eject Signal')
                plt.plot(t, receive_signal, label='Receive Signal')
                
                plt.plot(t[ej_peaks], eject_signal[ej_peaks], 'rx', label='Peaks')
                plt.plot(t[rc_peaks], receive_signal[rc_peaks], 'rx', label='Peaks')
                
                plt.annotate(f'Peak \n({t[rc_peaks[key_peak]]:.3e}, {receive_signal[rc_peaks[key_peak]]:.3e})',
                    xy=(t[rc_peaks[key_peak]], receive_signal[rc_peaks[key_peak]]), xycoords='data',
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
                plt.annotate(f'Peak \n({t[ej_peaks[0]]:.3e}, {eject_signal[ej_peaks[0]]:.3e})',
                    xy=(t[ej_peaks[0]], eject_signal[ej_peaks[0]]), xycoords='data',
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
                # plt.annotate(f'Delta = {t[ej_peaks[0]] - t[rc_peaks[key_peak]]:.2e}',
                #  xy=((t[ej_peaks[0]] + t[rc_peaks[key_peak]]) / 2, (receive_signal[rc_peaks[key_peak]] + eject_signal[ej_peaks[0]]) / 2),
                #  xycoords='data', textcoords='offset points',
                #  arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
                plt.plot([t[rc_peaks[key_peak]] ,t[ej_peaks[0]]], [receive_signal[rc_peaks[key_peak]], eject_signal[ej_peaks[0]]], 'r--')
                t_mid = (t[rc_peaks[key_peak]] + t[ej_peaks[0]]) / 2
                y_mid = (receive_signal[rc_peaks[key_peak]] + eject_signal[ej_peaks[0]]) / 2
                delta_t = abs(t[ej_peaks[0]] - t[rc_peaks[key_peak]])
                
                # slope = (abs(receive_signal[rc_peaks[key_peak]] - eject_signal[ej_peaks[0]])) / delta_t
                # rotation_angle = np.degrees(np.arctan(slope))
                
                plt.text(t_mid, y_mid, f'Time = {delta_t:.2e}', color='k', ha='center', va='center')
                
                plt.xlabel('Time')
                plt.ylabel('Amplitude')
                plt.legend()
                plt.title("{}, {}Hz".format(label ,frequency[random_index]))
                plt.show()
                
                flight_time.append(delta_t)
                
            elif 'S2P' in file and 'MC' in file:
                
                label = 'Mutual Coupling'
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequency = s_df['Frequency'].values
                phase = s_df['S21_phase'].values
                S21_amp = s_df['S21_amp'].values
                
                random_index = random.randint(0, len(frequency) - 1)
                random_index = -30
                
                eject_signal = np.cos(2 * np.pi * frequency[random_index] * t)
                receive_signal  = logmag2liner(S21_amp[random_index]) * np.cos(2 * np.pi * frequency[random_index] * t + phase[random_index])
                
                rc_peaks, _ = scipy.signal.find_peaks(receive_signal, height=0)
                ej_peaks, _ = scipy.signal.find_peaks(eject_signal, height=0)
                
                if rc_peaks[0] - ej_peaks[0] > rc_peaks[1] - ej_peaks[0]:
                    key_peak = 1
                else:
                    key_peak = 0
                
                plt.figure(figsize=(8, 5))
                plt.plot(t, eject_signal, label='Eject Signal')
                plt.plot(t, receive_signal, label='Receive Signal')
                
                plt.plot(t[ej_peaks], eject_signal[ej_peaks], 'rx', label='Peaks')
                plt.plot(t[rc_peaks], receive_signal[rc_peaks], 'rx', label='Peaks')
                
                plt.annotate(f'Peak \n({t[rc_peaks[key_peak]]:.3e}, {receive_signal[rc_peaks[key_peak]]:.3e})',
                    xy=(t[rc_peaks[key_peak]], receive_signal[rc_peaks[key_peak]]), xycoords='data',
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
                plt.annotate(f'Peak \n({t[ej_peaks[0]]:.3e}, {eject_signal[ej_peaks[0]]:.3e})',
                    xy=(t[ej_peaks[0]], eject_signal[ej_peaks[0]]), xycoords='data',
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
                plt.annotate(f'Delta = {t[ej_peaks[0]] - t[rc_peaks[key_peak]]:.2e}',
                 xy=((t[ej_peaks[0]] + t[rc_peaks[key_peak]]) / 2, (receive_signal[rc_peaks[key_peak]] + eject_signal[ej_peaks[0]]) / 2),
                 xycoords='data', textcoords='offset points',
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
                plt.plot([t[rc_peaks[key_peak]] ,t[ej_peaks[0]]], [receive_signal[rc_peaks[key_peak]], eject_signal[ej_peaks[0]]], 'r--')
                t_mid = (t[rc_peaks[key_peak]] + t[ej_peaks[0]]) / 2
                y_mid = (receive_signal[rc_peaks[key_peak]] + eject_signal[ej_peaks[0]]) / 2
                delta_t = abs(t[ej_peaks[0]] - t[rc_peaks[key_peak]])
                
                # slope = (abs(receive_signal[rc_peaks[key_peak]] - eject_signal[ej_peaks[0]])) / delta_t
                # rotation_angle = np.degrees(np.arctan(slope))
                
                plt.text(t_mid, y_mid, f'Time = {delta_t:.2e}', color='k', ha='center', va='center')
                
                plt.xlabel('Time')
                plt.ylabel('Amplitude')
                plt.legend()
                plt.title("{}, {}Hz".format(label ,frequency[random_index]))
                plt.show()
                
                base_time = delta_t
                
                
    flight_time = np.array(flight_time) - base_time
    
    sort_indices = sorted(range(len(labels)), key=lambda k: int(labels[k][:-2]))
    
    labels = np.array(labels)[sort_indices]
    flight_time = np.array(flight_time)[sort_indices]
    
    ref_time = []
    
    for dis in labels:
        dis = float(dis[:-2]) * 10 ** -2
        time = dis / 3e8 * 2
        ref_time.append(time)
                 
    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 14})
    plt.plot(labels, flight_time, 'o-', label='Flight Time')
    plt.plot(labels, ref_time, 'o-', label='Ground Truth')
    
    plt.xlabel('Distance', fontsize=18)
    plt.ylabel('Time', fontsize=18)
    plt.title('Time Comparsion', fontsize=18)
    plt.legend()
    
    plt.show()
    
                
                
                
                