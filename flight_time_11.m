clear all;clc;close all;

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

fc = {1e7, 2*1e7, 3*1e7, 4*1e7, 5*1e7, 6*1e7, 7*1e7, 8*1e7, 9*1e7, 1e8, 2*1e8, 3*1e8, 4*1e8, 5*1e8};

t = signal(:,1);
fs = 1/(t(2)-t(1));

signal = signal(:,2);

figure;

colors = jet(length(fc));

hLine = plot(t, signal, 'LineWidth', 2, 'Color', [0, 0.4470, 0.7410, 0.2], 'DisplayName', 'Signal');
hold on;

hLineEnv = cell(length(fc), 1);

for i = 1:length(fc)

    analytical = hilbert(signal);
    env = abs(analytical);

    [b, a] = butter(3, fc{i}/(fs/2), 'low');
    env = filtfilt(b, a, env);

    hLineEnv{i} = plot(t, env, 'LineWidth', 2, 'Color', colors(i,:), 'DisplayName', ['Envelope, fc = ', num2str(fc{i})]');
    hold on;

end

hold off;

legend('show');
xlabel('Time (s)');
ylabel('Magnitude');
title('Envelope Detection, by different cut-off frequency lowpass filter');

popupmenu = uicontrol('Style', 'popupmenu', 'String', fc, 'Position', [20 340 100 50], 'Callback', @(src, event) updatePlot(src, event, hLine, hLineEnv));

function updatePlot(source, ~, hLine, hLineEnv)

    selectedCurve = get(source, 'Value');

    set(hLine, 'Visible', 'on');
    for i = 1:length(hLineEnv)
        if i ~= selectedCurve
            set(hLineEnv{i}, 'Visible', 'off');
        else
            set(hLineEnv{i}, 'Visible', 'on');
        end
    end
end



