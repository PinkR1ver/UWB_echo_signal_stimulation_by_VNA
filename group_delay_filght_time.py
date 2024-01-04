"""
This file is to calculate groupy delay and then yield the filght time for each flight
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from rich.progress import track

def custom_sort(label):
    # 提取标签中的数字部分并转换为整数
    return int(label[:-2])  # 去掉末尾的"cm"并转换为整数

def sp_detect(signal, window_size=5):
    
    for i in range(window_size, len(signal) - window_size):
        
        window_mean = 0
        
        for j in range(i - window_size, i):
            window_mean += abs(signal[j])
    
        for j in range(i + 1, i + window_size + 1):
            window_mean += abs(signal[j])
            
        window_mean = window_mean / (2 * window_size)
        
        replace_mean = 0 
        
        for j in range(i - window_size, i):
            replace_mean += signal[j]
            
        for j in range(i + 1, i + window_size + 1):
            replace_mean += signal[j]
            
        replace_mean = replace_mean / (2 * window_size)
        
        if abs(signal[i]) > 3 * window_mean:
            
            signal[i] = replace_mean
        
    return signal

if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    
    labels = []
    delay_time = []
    
    for root, dirs, files in os.walk(data_path):
        for file in track(files, description='Calculating Group Delay...', total=len(files) - 2):
            
            if "S2P" in file and file.split('.')[0].isdigit():
                
                label = file.split('.')[0] + 'cm'
                labels.append(label)
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])

                phase = s_df['S21_phase'].values
                freqency = s_df['Frequency'].values
                
                # Calculate the group delay
                # using interpolation to increase the resolution of the phase
                
                # phase = np.unwrap(phase)
                # phase = np.interp(np.linspace(0, 1, 1000000), np.linspace(0, 1, len(phase)), phase)
                # freqency = np.interp(np.linspace(0, 1, 1000000), np.linspace(0, 1, len(freqency)), freqency)
                
                group_delay = np.diff(phase) / np.diff(freqency)
                group_delay = sp_detect(group_delay)
                
                group_delay = group_delay[20:-20]
                freqency = freqency[20:-20]
                phase = phase[20:-20]
                
                delay_time.append(np.median(group_delay))
                
                # cut the suddenly pulse group delay value
                
                # plot the group delay
                
                plt.figure(figsize=(8, 5))
                
                plt.subplot(2, 1, 1)
                plt.plot(freqency[1:], group_delay)
                plt.ylabel('Group Delay')
                plt.title('Group Delay and Phase {}'.format(label))
                
                plt.subplot(2, 1, 2)
                plt.plot(freqency, phase)
                
                plt.xlabel('Frequency')
                plt.ylabel('Phase')
                plt.tight_layout()
                
                plt.savefig(os.path.join(base_path, 'fig', file.split('.')[0] + 'group_delay' + '.png'))
                
            else:
                
                s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])

                phase = s_df['S21_phase'].values
                freqency = s_df['Frequency'].values
                
                # Calculate the group delay
                # using interpolation to increase the resolution of the phase
                
                # phase = np.unwrap(phase)
                # phase = np.interp(np.linspace(0, 1, 1000000), np.linspace(0, 1, len(phase)), phase)
                # freqency = np.interp(np.linspace(0, 1, 1000000), np.linspace(0, 1, len(freqency)), freqency)
                
                group_delay = np.diff(phase) / np.diff(freqency)
                group_delay = sp_detect(group_delay)
                
                group_delay = group_delay[20:-20]
                freqency = freqency[20:-20]
                phase = phase[20:-20]
                
                base_delay = np.median(group_delay)
                
                # cut the suddenly pulse group delay value
                
                # plot the group delay
                
                plt.figure(figsize=(8, 5))
                
                plt.subplot(2, 1, 1)
                plt.plot(freqency[1:], group_delay)
                plt.ylabel('Group Delay')
                plt.title('Group Delay and Phase {}'.format(file.split('.')[0]))
                
                plt.subplot(2, 1, 2)
                plt.plot(freqency, phase)
                
                plt.xlabel('Frequency')
                plt.ylabel('Phase')
                plt.tight_layout()
                
                plt.savefig(os.path.join(base_path, 'fig', file.split('.')[0] + 'group_delay' + '.png'))
                
    
    # sort label by its digit value
    
    delay_time = np.array(delay_time) - base_delay
    
    sort_indices = sorted(range(len(labels)), key=lambda k: int(labels[k][:-2]))
    
    labels = np.array(labels)[sort_indices]
    delay_time = np.array(delay_time)[sort_indices]
    
    # plot the delay time
    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 14})
    plt.plot(labels, delay_time, 'o-', label='Group Delay')
    flight_time = []
    
    for dis in labels:
        dis = float(dis[:-2]) * 10 ** -2
        time = dis / 3e8 * 2
        flight_time.append(time)
    
    plt.plot(labels, flight_time, 'o-', label='Flight Time')
    
    plt.legend()
    plt.xlabel('Distance', fontsize=18)
    plt.ylabel('Time', fontsize=18)
    plt.title('Time Comparsion', fontsize=18)
    
    plt.show()
    
    
    
                
                


