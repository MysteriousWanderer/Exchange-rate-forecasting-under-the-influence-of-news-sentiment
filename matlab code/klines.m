% 读取Excel文件中的数据
data = readtable('data.xlsx','range','B2:E71');
data = table2array(data);
data = flipud(data);
%% 

% 提取收盘价、开盘价、最高价和最低价数据
close_price = data(:, 1);
open_price = data(:, 2);
high_price = data(:, 3);
low_price = data(:, 4);

% 创建一个新的图形窗口
figure;

% 绘制K线图和长方形
for i = 1:length(close_price)
    if close_price(i) > open_price(i)
        % 阳线，用绿色标记
        line([i, i], [low_price(i), high_price(i)], 'Color', '#62AA67');
        rectangle('Position', [i-0.4, open_price(i), 0.8, close_price(i)-open_price(i)], 'FaceColor', '#A4D09D');
    else
        % 阴线，用红色标记
        line([i, i], [low_price(i), high_price(i)], 'Color', '#E44A33');
        rectangle('Position', [i-0.4, close_price(i), 0.8, open_price(i)-close_price(i)], 'FaceColor', '#E44A33');
    end
    
    % 绘制下影线和上影线（黑色）
    line([i, i], [low_price(i), min(open_price(i), close_price(i))], 'Color', 'k','LineWidth',0.6);
    line([i, i], [high_price(i), max(open_price(i), close_price(i))], 'Color', 'k','LineWidth',0.6);
end

% 设置图形标题和轴标签
title('USD/CNY K线图','FontSize',16);
xlabel('日期','FontSize',16);
ylabel('价格USD/CNY','FontSize',16);

% 设置X轴刻度
xticks([1,21,42,62]);
xticklabels({'11月','12月','1月','2月'});
ax = gca;
ax.XAxis.FontSize = 14; % 设置刻度字体大小
ax.YAxis.FontSize = 14; % 设置刻度字体大小
% 显示图形
grid off;