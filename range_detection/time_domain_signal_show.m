clear all;clc;close all;

file_path = './signal/signal.xlsx';
signal = readmatrix(file_path);

dis = signal(1, 3:end); % get distance
dis = num2cell(dis);

signal = signal(2:end,:); % delete first row
t = signal(:, 1); % get t
mc_signal = signal(:,2); % get mutual coupling signal

signal = signal(:, 3:end);

[~, t0_index] = max(mc_signal);

anchor_offset = cell(length(dis), 1);
anchor_offset_time = cell(length(dis), 1);
[~, mc_signal_anchor] = max(mc_signal(1:t0_index));
for i = 1:length(dis)
    [~, signal_anchor] = max(signal(1:t0_index, i));
    anchor_offset{i} = signal_anchor - mc_signal_anchor;
    anchor_offset_time{i} = (signal_anchor - mc_signal_anchor) * (t(2) - t(1));
end

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

anchor_offset_YData = cell(length(signal), 1);
offset_YData = cell(length(signal), 1);
original_YData = cell(length(signal), 1);

for i = 1:length(dis)
    if anchor_offset{i} > 0
        mc_signal_offset = zeros(1, length(hLine.YData));
        mc_signal_offset(anchor_offset{i} + 1:end) = hLine.YData(anchor_offset{i} + 1:end);
        anchor_offset_YData{i} = hLineEnv{i}.YData - mc_signal_offset;
    else
        mc_signal_offset = zeros(1, length(hLine.YData));
        mc_signal_offset(1:end + anchor_offset{i}) = hLine.YData(-anchor_offset{i} + 1:end);
        anchor_offset_YData{i} = hLineEnv{i}.YData - mc_signal_offset;
    end 
end

for i = 1:length(dis)
    offset_YData{i} = hLineEnv{i}.YData - hLine.YData;
end

for i = 1:length(dis)
    original_YData{i} = hLineEnv{i}.YData;
end

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

button = uicontrol('Style', 'pushbutton', 'String', 'Delete Background', 'Position', [320, 20, 100, 50], 'Callback', @(src, event) deleteBackgroundNoise(src, event, hLine, hLineEnv, offset_YData, original_YData));
button2 = uicontrol('Style', 'pushbutton', 'String', 'Delete Background with Anchor', 'Position', [420, 20, 100, 50], 'Callback', @(src, event) deleteBackgroundNoise_Anchor(src, event, hLine, hLineEnv, anchor_offset_YData, original_YData));

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


function deleteBackgroundNoise_Anchor(~, ~, ~, hLineEnv, anchor_offset_YData, original_YData)

    persistent flag;

    if isempty(flag)
        flag = 1;
    end

    if flag

        for i = 1:length(hLineEnv)
            set(hLineEnv{i}, 'YData', anchor_offset_YData{i})
        end

        flag = 0;

    else

        for i = 1:length(hLineEnv)
            set(hLineEnv{i}, 'YData', original_YData{i})
        end

        flag = 1;

    end


end


function deleteBackgroundNoise(~, ~, ~, hLineEnv, offset_YData, original_YData)

    persistent flag;

    if isempty(flag)
        flag = 1;
    end

    if flag

        % delete signal a hLine
        for i = 1:length(hLineEnv)
            set(hLineEnv{i}, 'YData', offset_YData{i})
        end

        flag = 0;

    else

        % delete signal a hLine
        for i = 1:length(hLineEnv)
            set(hLineEnv{i}, 'YData', original_YData{i})
        end

        flag = 1;

    end


end