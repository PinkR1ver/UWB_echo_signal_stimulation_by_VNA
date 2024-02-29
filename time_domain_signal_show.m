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



prompt = dis;
for i = 1:length(dis)
    prompt{i} = ['Show Signal in Dis = ', num2str(dis{i}), 'cm', ' and MC signal'];
end
prompt{end + 1} = 'Show All Signal';

popupmenu1 = uicontrol('Style', 'popupmenu', 'String', prompt, 'Position', [20, 20, 100, 50], 'Callback', @(src, event) updatePlot1(src, event, hLine, hLineEnv));

for i = 1:length(dis)
    dis{i} = ['Show Signal in Dis = ', num2str(dis{i}), 'cm'];
end
prompt{end} = 'Show Background Signal';

popupmenu2 = uicontrol('Style', 'popupmenu', 'String', prompt, 'Position', [120, 20, 100, 50], 'Callback', @(src, event) updatePlot2(src, event, hLine, hLineEnv));

for i = 1:length(dis)
    prompt{i} = ['Hide Signal in Dis = ', num2str(dis{i}), 'cm'];
end
prompt{end} = 'Hide Background Signal';

popupmenu3 = uicontrol('Style', 'popupmenu', 'String', prompt, 'Position', [220, 20, 100, 50], 'Callback', @(src, event) updatePlot3(src, event, hLine, hLineEnv));

% make a button to delete all signal a mc_signal

button = uicontrol('Style', 'pushbutton', 'String', 'Delete Background', 'Position', [320, 20, 100, 50], 'Callback', @(src, event) deleteBackgroundNoise(src, event, hLine, hLineEnv));

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

    for i = 1:length(hLineEnv)
        if i == selectedCurve
            set(hLineEnv{i}, 'Visible', 'on');
        end
    end

    if selectedCurve == length(hLineEnv) + 1
        set(hLine, 'Visible', 'on');
    end

end

function updatePlot3(source, ~, hLine, hLineEnv)

    selectedCurve = get(source, 'Value');

    for i = 1:length(hLineEnv)
        if i == selectedCurve
            set(hLineEnv{i}, 'Visible', 'off');
        end
    end

    if selectedCurve == length(hLineEnv) + 1
        set(hLine, 'Visible', 'off');
    end
end


function deleteBackgroundNoise(~, ~, hLine, hLineEnv)

    persistent flag;

    if isempty(flag)
        flag = 1;
    end

    if flag

        % delete signal a hLine
        for i = 1:length(hLineEnv)
            set(hLineEnv{i}, 'YData', hLineEnv{i}.YData - hLine.YData)
        end

        flag = 0;

    else

        % delete signal a hLine
        for i = 1:length(hLineEnv)
            set(hLineEnv{i}, 'YData', hLineEnv{i}.YData + hLine.YData)
        end

        flag = 1;

    end


end