clear all;clc;close all;

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

t = signal(:,1);
fs = 1/(t(2)-t(1));

signal = signal(:,2);

np = {100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 5000, 7500, 10000, 15000, 20000};


figure;
set(0, 'DefaultAxesFontSize', 14);

colors = jet(length(np)); % Create a colormap with as many colors as there are elements in np

hLine = plot(t, signal, 'LineWidth', 2, 'Color', [0, 0.4470, 0.7410], 'DisplayName', 'Signal');
hold on;

hLineEnv = cell(length(np), 1);

for i = 1:length(np)

    [up, ~] = envelope(signal, np{i}, 'peak');
    env = up;

    hLineEnv{i} = plot(t, env, 'LineWidth', 2, 'Color', colors(i,:), 'DisplayName', ['Envelope, np = ', num2str(np{i})]');
    hold on;

end

hold off;

legend('show');
xlabel('Time (s)');
ylabel('Magnitude');
title('Envelope, peak method, different np samples')

np{end + 1} = 'all';

% write a popmenu to select the np value

popupmenu = uicontrol('Style', 'popupmenu', 'String', np, 'Position', [20 340 100 50], 'Callback', @(src, event) updatePlot(src, event, hLine, hLineEnv));

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



