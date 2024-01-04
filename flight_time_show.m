clear all;clc;close all;

label = {'t', '05cm', '08cm', '100cm', '12cm', '16cm', '20cm', '24cm', '28cm', '32cm', '36cm', '40cm', '45cm', '50cm', '55cm', '60cm', '65cm', '70cm', '75cm', '80cm', '85cm', '90cm', '95cm'};

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

t = signal(:,1);
fs = 1/(t(2)-t(1));

s = signal(:,2);

analytical = hilbert(s);
env = abs(analytical);

figure;
set(0, 'DefaultAxesFontSize', 14);

plot(t, s, 'Color', [0, 0.4470, 0.7410, 0.5]);
hold on;
plot(t, env, 'r', 'LineWidth', 1);
hold off;
xlabel('Time (s)');
ylabel('Amplitude');
title('Time Domain Signal in 5cm');
legend('Signal', 'Envelope');


