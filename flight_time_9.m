clear all;clc;close all;

label = {'t', '05cm', '08cm', '100cm', '12cm', '16cm', '20cm', '24cm', '28cm', '32cm', '36cm', '40cm', '45cm', '50cm', '55cm', '60cm', '65cm', '70cm', '75cm', '80cm', '85cm', '90cm', '95cm'};

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

t = signal(:,1);
fs = 1/(t(2)-t(1));

fc = 1e8;
[b, a] = butter(3, fc/(fs/2), 'low');

for i = 2:length(label)

    s = signal(:,i);
    
    analytical = hilbert(s);
    env = abs(analytical);

    env_filtered = filtfilt(b, a, env);
    
    env2 = env;
    for j = 1:10
        analytical = hilbert(env2);
        env2 = abs(analytical);
    end

    [up, ~] = envelope(s, 300,'rms');
    env3 = up;

    [up, ~] = envelope(s, 2000, 'peak');
    env4 = up;

    figure();
    subplot(5,1,1);
    plot(t, s, 'b', t, env, 'r', 'LineWidth', 2);
    ylabel('Amplitude');
    xlabel('Time (s)');
    title(label{i})
    legend('Signal', 'Envelope');

    subplot(5,1,2);
    plot(t, s, 'b', t, env_filtered, 'r', 'LineWidth', 2);
    ylabel('Amplitude');
    xlabel('Time (s)');
    title(label{i})
    legend('Signal', 'Envelope Filtered', 'LineWidth', 2);

    subplot(5,1,3);
    plot(t, env, 'b', t, env2, 'r');
    ylabel('Amplitude');
    xlabel('Time (s)');
    legend('Envelope', 'Envelope of Envelope', 'LineWidth', 2);


    subplot(5,1,4);
    plot(t, s, 'b', t, env3, 'r');
    xlabel('Time (s)');
    ylabel('Amplitude');
    legend('Signal', 'Envelope RMS', 'LineWidth', 2);

    subplot(5,1,5);
    plot(t, s, 'b', t, env4, 'r');
    xlabel('Time (s)');
    ylabel('Amplitude');
    legend('Signal', 'Envelope Peak', 'LineWidth', 2);

    
end

figure();
flag = 0;

for i = 2:10

    if i == 4
        flag = 1;
        continue;
    end
    
    s = signal(:,i);
    
    [up, ~] = envelope(s, 2000, 'peak');
    env = up;

    if flag
        subplot(8, 1, i-2)
    else
        subplot(8, 1, i-1)
    end
    
    plot(t, env, 'LineWidth', 2);
    ylabel('Amplitude');
    xlabel('Time (s)');
    title(label{i})
    
end