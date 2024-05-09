clear,clc;
% 读取Excel文件中的数据
data = readtable('data.xlsx','range','B2:E619');
data = table2array(data);
% 提取收盘价、开盘价、最高价和最低价数据
close_price = data(:, 1);
open_price = data(:, 2);
high_price = data(:, 3);
low_price = data(:, 4);

% 计算平均值
avg_close = mean(close_price);
avg_open = mean(open_price);
avg_high = mean(high_price);
avg_low = mean(low_price);

% 计算标准差
std_close = std(close_price);
std_open = std(open_price);
std_high = std(high_price);
std_low = std(low_price);

% 计算最小值
min_close = min(close_price);
min_open = min(open_price);
min_high = min(high_price);
min_low = min(low_price);

% 计算最大值
max_close = max(close_price);
max_open = max(open_price);
max_high = max(high_price);
max_low = max(low_price);

% 计算峰度和偏度
kurt_close = kurtosis(close_price);
kurt_open = kurtosis(open_price);
kurt_high = kurtosis(high_price);
kurt_low = kurtosis(low_price);

skew_close = skewness(close_price);
skew_open = skewness(open_price);
skew_high = skewness(high_price);
skew_low = skewness(low_price);

% 绘制箱线图，并指定箱线图的颜色
figure;
boxplot([close_price, open_price, high_price, low_price], 'Labels', {'收盘', '开盘', '高', '低'});
title('USD/CNY汇率K线箱型图','FontSize',16);

h = findobj(gca,'Tag','Box');
for j=1:length(h)
    set(h(j),'Color','#547DB1','LineWidth',1);
end

h = findobj(gca,'Tag','Median');
for j=1:length(h)
    set(h(j),'Color','#A4D09D','LineWidth',2);
end
