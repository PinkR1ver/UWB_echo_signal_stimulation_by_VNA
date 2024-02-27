clear;clc;close all;

file = '.\data\05.S2P';

[freq, S11_amp, S21_amp, S11_phase, S21_phase] = S2P_read(file)