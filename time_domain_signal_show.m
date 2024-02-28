clear all;clc;close all;

file_path = './signal/signal.xlsx';
signal = readmatrix(file_path);

signal = signal(2:end,:); % delete first row
t = signal(:, 1); % get t
mc_signal = signal(:,2); % get mutual coupling signal

signal = signal(:, 3:end);

dis = {5, 8, 12, 16, 20, 24, 28, 32, 36, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95};

figure;

hLine = plot(t, mc_signal, 'LineWidth', 1.5, 'DisplayName', 'MC signal');
hold on;

hLineEnv = cell(length(dis), 1);

for i = 1:length(dis)

    hLineEnv{i} = plot(t, signal(:,i), 'LineWidth', 1.5, 'DisplayName', ['Dis = ', num2str(dis{i}), 'cm']);
    hold on;

end

hold off;

legend('show');
xlabel('Time (s)');
ylabel('Magnitude');
title('Background noise and signal in different distances');

grid on;
grid minor;

% get a popupmenus to control which show, which not show

dis{end+1} = 'all';

popupmenu1 = uicontrol('Style', 'popupmenu', 'String', dis, 'Position', [20, 20, 100, 50], 'Callback', @(src, event) updatePlot1(src, event, hLine, hLineEnv));
popupmenu2 = uicontrol('Style', 'popupmenu', 'String', dis, 'Position', [120, 20, 100, 50], 'Callback', @(src, event) updatePlot2(src, event, hLine, hLineEnv));
popupmenu3 = uicontrol('Style', 'popupmenu', 'String', dis, 'Position', [220, 20, 100, 50], 'Callback', @(src, event) updatePlot3(src, event, hLine, hLineEnv));

function updatePlot1(source, ~, hLine, hLineEnv)

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

function updatePlot2(source, ~, hLine, hLineEnv)

    selectedCurve = get(source, 'Value');

    set(hLine, 'Visible', 'on');

    for i = 1:length(hLineEnv)
        if i == selectedCurve
            set(hLineEnv{i}, 'Visible', 'on');
        end
    end
end

function updatePlot3(source, ~, hLine, hLineEnv)

    selectedCurve = get(source, 'Value');

    set(hLine, 'Visible', 'on');

    for i = 1:length(hLineEnv)
        if i == selectedCurve
            set(hLineEnv{i}, 'Visible', 'off');
        end
    end
end