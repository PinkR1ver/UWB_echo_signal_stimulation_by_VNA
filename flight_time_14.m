clear all;clc;close all;

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

t = signal(:,1);
fs = 1/(t(2)-t(1));

signal = signal(:,2);

fl = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 400, 500, 1000, 2000, 5000, 10000};


figure;
set(0, 'DefaultAxesFontSize', 14);

colors = jet(length(fl)); % Create a colormap with as many colors as there are elements in fl

hLine = plot(t, signal, 'LineWidth', 2, 'Color', [0, 0.4470, 0.7410], 'DisplayName', 'Signal');
hold on;

hLineEnv = cell(length(fl), 1);

for i = 1:length(fl)

    [up, ~] = envelope(signal, fl{i}, 'analytic');
    env = up;

    hLineEnv{i} = plot(t, env, 'LineWidth', 2, 'Color', colors(i,:), 'DisplayName', ['Envelope, fl = ', num2str(fl{i})]');
    hold on;

end

hold off;

legend('show');
xlabel('Time (s)');
ylabel('Magnitude');
title('Envelope, Hilbert filter method, different fl samples')

% write a popmenu to select the fl value
fl{end + 1} = 'all';

popupmenu = uicontrol('Style', 'popupmenu', 'String', fl, 'Position', [20 340 100 50], 'Callback', @(src, event) updatePlot(src, event, hLine, hLineEnv));

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

    if selectedCurve == length(hLineEnv) + 1
        for i = 1:length(hLineEnv)
            set(hLineEnv{i}, 'Visible', 'on');
        end
    end
end



