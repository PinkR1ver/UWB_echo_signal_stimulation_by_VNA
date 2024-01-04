% 创建一个简单的图形
figure;

% 创建曲线数据
x = linspace(0, 2*pi, 100);
y1 = sin(x);
y2 = cos(x);
y3 = tan(x);

% 绘制所有曲线并保存曲线句柄
hLine1 = plot(x, y1, 'LineWidth', 2, 'DisplayName', 'sin(x)');
hold on;
hLine2 = plot(x, y2, 'LineWidth', 2, 'DisplayName', 'cos(x)');
hLine3 = plot(x, y3, 'LineWidth', 2, 'DisplayName', 'tan(x)');
hold off;

% 添加图例
legend('show');

% 创建滑动条
slider = uicontrol('Style', 'slider', 'Min', 1, 'Max', 3, 'Value', 1, 'SliderStep', [1/2 1], 'Position', [20 20 200 20], 'Callback', @(src, event) updatePlot(src, event, hLine1, hLine2, hLine3));

% 回调函数，根据滑动条值更新曲线的可见性
function updatePlot(source, ~, hLine1, hLine2, hLine3)
    % 获取滑动条的值
    sliderValue = round(get(source, 'Value'));
    
    % 根据滑动条值设置曲线的可见性
    switch sliderValue
        case 1
            set(hLine1, 'Visible', 'on');
            set(hLine2, 'Visible', 'off');
            set(hLine3, 'Visible', 'off');
        case 2
            set(hLine1, 'Visible', 'off');
            set(hLine2, 'Visible', 'on');
            set(hLine3, 'Visible', 'off');
        case 3
            set(hLine1, 'Visible', 'off');
            set(hLine2, 'Visible', 'off');
            set(hLine3, 'Visible', 'on');
    end
end
