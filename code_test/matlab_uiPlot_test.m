% 创建一个简单的图形
figure;

% 创建一个按钮
button = uicontrol('Style', 'pushbutton', 'String', '改变颜色', 'Callback', @changeColor);

% 回调函数，定义按钮按下时执行的操作
function changeColor(~, ~)
    % 生成随机颜色
    newColor = rand(1, 3);
    
    % 获取当前图形句柄
    hFig = gcf;
    
    % 改变图形的背景颜色
    set(hFig, 'Color', newColor);
end
