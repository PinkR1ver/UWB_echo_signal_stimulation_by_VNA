clear all;clc;close all;

file_path = './data/time_domain_signal.csv';
signal = readmatrix(file_path);

t = signal(:,1);
fs = 1/(t(2)-t(1));

signal = signal(:,2);

wl = {10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1500, 2000, 3000, 4000, 5000, 10000, 20000};


figure;
set(0, 'DefaultAxesFontSize', 14);


colors = jet(length(wl)); % Create a colormap with as many colors as there are elements in wl

hLine = plot(t, signal, 'LineWidth', 2, 'Color', [0, 0.4470, 0.7410], 'DisplayName', 'Signal');
hold on;

hLineEnv = cell(length(wl), 1);

for i = 1:length(wl)

    [up, ~] = envelope(signal, wl{i}, 'analytic');
    env = up;

    hLineEnv{i} = plot(t, env, 'LineWidth', 2, 'Color', colors(i,:), 'DisplayName', ['Envelope, wl = ', num2str(wl{i})]');
    hold on;

end

hold off;

legend('show');
xlabel('Time (s)');
ylabel('Magnitude');
title('Envelope, RMS method, different wl samples')

% write a popmenu to select the wl value
wl{end + 1} = 'all';

popupmenu = uicontrol('Style', 'popupmenu', 'String', wl, 'Position', [20 340 100 50], 'Callback', @(src, event) updatePlot(src, event, hLine, hLineEnv));

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



