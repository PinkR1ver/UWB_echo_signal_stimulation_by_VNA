import streamlit as st
import pandas as pd 
import numpy as np 
import os
import matplotlib.pyplot as plt 
from rich.progress import track
from scipy import io
from bokeh.plotting import figure

def logmag2liner(x):
    return 10 ** (x/2)


def read_s2p_file(file_path, start_index=3161):
    
    df = pd.read_csv(file_path, skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
    frequency = df['Frequency'].values
    phase = df['S21_phase'].values
    amp = df['S21_amp'].values
    
    return frequency, phase, amp


def freq2time(frequency, phase, amp, t):
        
        signal = np.zeros(len(t))
        count = 0
        
        for ph, am, freq in zip(phase, amp, frequency):
            signal += logmag2liner(am) * np.cos(2 * np.pi * freq * t + ph/180 * np.pi)
            count += 1
            
        signal = signal / count
        
        return signal

def color_platte():
    
    # need 30 color
    
    return ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data')
    
    with st.sidebar:
        
        data_select = st.multiselect('Select the files to get the system delay time', os.listdir(data_path), ['MC.S2P', '08.S2P', '12.S2P', '16.S2P', '20.S2P'])
        validation_select = st.multiselect('Select the files to validate the system delay time', os.listdir(data_path), ['24.S2P'])
        
        
    st.title('Antenna Delay Calibration in an IR-UWB Radar Simulated by Vector Network Analyzer')
    st.markdown('This is a web application for the project "Antenna Delay Calibration in an IR-UWB Radar Simulated by Vector Network Analyzer".')
                
    st.markdown('## First Step, Get the $S_{21}$ scattering parameters from VNA')
        
    if data_select:
        
        fig1 = figure(title='S21 Amp', x_axis_label='Frequency', y_axis_label='Amplitude')
        fig2 = figure(title='S21 Phase', x_axis_label='Frequency', y_axis_label='Phase')
        
        freq_list = []
        phase_list = []
        amp_list = []
        label_list = []
        
        mc_freq = []
        mc_phase = []
        mc_amp = []
        
        for index, file in enumerate(data_select):
            
            frequency, phase, amp = read_s2p_file(os.path.join(data_path, file), 0)
            
            if file != 'MC.S2P':
                fig1.line(frequency, amp, legend_label=(file.split('.')[0] + 'cm'), color=color_platte()[index])
                fig2.line(frequency, phase, legend_label=(file.split('.')[0] + 'cm'), color=color_platte()[index])
                
                frequency, phase, amp = read_s2p_file(os.path.join(data_path, 'MC.S2P'))
                freq_list.append(frequency)
                phase_list.append(phase)
                amp_list.append(amp)
                label_list.append(file.split('.')[0] + 'cm')
                
            else:
                fig1.line(frequency, amp, legend_label='MC', color=color_platte()[index])
                fig2.line(frequency, phase, legend_label='MC', color=color_platte()[index])
                
                frequency, phase, amp = read_s2p_file(os.path.join(data_path, 'MC.S2P'))
                mc_freq = frequency
                mc_phase = phase
                mc_amp = amp
                
            
        st.bokeh_chart(fig1)
        st.bokeh_chart(fig2)
        
        st.markdown('## Second step, convert the $S_{21}$ to time domain signal')
        st.markdown("$$\sum_{i}^{N} S_{21_{i}} sin(\omega_{i}t + \phi_{i})$$")
        
        signal_df = pd.read_excel(os.path.join(base_path, 'signal', 'signal.xlsx'))
        t = signal_df['t'].values
        t = t[1:10000]
        mc_signal = signal_df['MC'].values
        mc_signal = mc_signal[1:10000]
            
        fig = figure(title='Time Domain Signal', x_axis_label='Time', y_axis_label='Magnitude')
        fig.line(t, mc_signal, legend_label='MC', color=color_platte()[0])
        
        for index, label in enumerate(label_list):
            
            ref = label.replace('cm', '')
            
            if ref[0] == '0':
                ref = ref[1:]
            ref = int(ref)
            signal  = signal_df[ref].values
            signal = signal[1:10000]
            
            fig.line(t, signal, legend_label=label, color=color_platte()[index])
            
        st.bokeh_chart(fig)
        
        st.markdown('## Third step, remove the MC signal from the other signal')
        
        fig = figure(title='Time Domain Signal', x_axis_label='Time', y_axis_label='Magnitude')
        t_peak = []
        
        for index, label in enumerate(label_list):
            
            ref = label.replace('cm', '')
            
            if ref[0] == '0':
                ref = ref[1:]
            ref = int(ref)
            signal  = signal_df[ref].values
            signal = signal[1:10000]
            
            signal = signal - mc_signal
            
            fig.line(t, signal, legend_label=label, color=color_platte()[index])
            # point the peak
            if index != len(label_list) - 1:
                fig.circle(t[np.argmax(signal)], np.max(signal), color='red')
            else:
                fig.circle(t[np.argmax(signal)], np.max(signal), legend='peak', color='red')
                
            t_peak.append(t[np.argmax(signal)])
            
        st.bokeh_chart(fig)
        
        
        st.markdown('## Fourth step, calculate the delay')
        st.markdown(r'$$t_{\text{peak}} = t_{\text{flight} + t_{\text{delay}}}$$')
        st.markdown(r'$$t_{\text{flight}} = \frac{\text{distance}}{c}$$')
        
        t_delay = []
        
        for label in label_list:
            
            distance = int(label.replace('cm', '')) * 1e-2
            t_flight = distance / 3e8
            
            t_delay_tmp = t_peak[label_list.index(label)] - t_flight
            t_delay_tmp = t_delay_tmp * 1e9
            t_delay.append(t_delay_tmp)
        
            
        t_delay_df = pd.DataFrame({'Distance(cm)': label_list, 'Delay(ns)': t_delay})
        st.dataframe(t_delay_df)
        
        t_delay_avg = np.mean(t_delay)
        st.write('The average delay is: ', t_delay_avg, 'ns')
        
        st.markdown('## Final step, validate the delay, see the method works')
        
        for validation in validation_select:
            
            ref = validation.replace('.S2P', '')
            if ref[0] == '0':
                ref = ref[1:]
            ref = int(ref)
            signal = signal_df[ref].values
            mc_signal = signal_df['MC'].values
            signal = signal - mc_signal
            t_peak = t[np.argmax(signal)]
            t_flight = t_peak - t_delay_avg * 1e-9
            predict_distance = t_flight * 3e8 / 2 * 1e2
            st.write('The predict distance for ', validation, ' is: ', predict_distance, 'cm')