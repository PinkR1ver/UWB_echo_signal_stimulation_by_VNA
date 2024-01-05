clear all;clc;close all;

label = {'t', '05cm', '08cm', '100cm', '12cm', '16cm', '20cm', '24cm', '28cm', '32cm', '36cm', '40cm', '45cm', '50cm', '55cm', '60cm', '65cm', '70cm', '75cm', '80cm', '85cm', '90cm', '95cm'};

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

t = signal(:,1);
fs = 1/(t(2)-t(1));

fc = 2*1e7;
[b, a] = butter(3, fc/(fs/2), 'low');

figure();
set(0, 'DefaultAxesFontSize', 14);

flag = 0;
max_value = -inf;
min_value = inf;

group_size = 4;

j = 1;

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
    
    subplot(4, 1, j);
    
    plot(t, env, 'LineWidth', 2);
    ylabel('Amplitude');
    xlabel('Time (s)');
    title(label{i})

    if j == group_size

        for k = 1:group_size
            subplot(group_size, 1, k);
            ylim([0.9 * min_value, 1.1 * max_value]);
        end

        max_value = -inf;
        min_value = inf;
           
        j = 0;
        figure();
    end

    j = j + 1;
end
