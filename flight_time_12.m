clear all;clc;close all;

label = {'t', '05cm', '08cm', '100cm', '12cm', '16cm', '20cm', '24cm', '28cm', '32cm', '36cm', '40cm', '45cm', '50cm', '55cm', '60cm', '65cm', '70cm', '75cm', '80cm', '85cm', '90cm', '95cm'};

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

t = signal(:,1);
fs = 1/(t(2)-t(1));

fc = 7*1e7;
[b, a] = butter(3, fc/(fs/2), 'low');

figure();
flag = 0;
max_value = -inf;
min_value = inf;

for i = 2:length(label)

    if i == 4
        flag = 1;
        continue;
    end
    
    s = signal(:,i);

    analytical = hilbert(s);
    env = abs(s);

    env = filtfilt(b, a, env);
    
    max_value = max(max_value, max(env));
    min_value = min(min_value, min(env));
    

    if flag
        subplot(length(label) - 2, 1, i-2)
    else
        subplot(length(label) - 2, 1, i-1)
    end
    
    plot(t, env, 'LineWidth', 2);
    ylabel('Amplitude');
    xlabel('Time (s)');
    title(label{i})
    
end

for i = 1:length(label) - 2
    subplot(length(label) - 2, 1, i);
    ylim([0.9 * min_value, 1.1 * max_value]);
end