clear, clc;

% 读取Excel文件中的数据
data = readtable('data.xlsx','range','B2:E619');
data = table2array(data);
data = flipud(data);
% 提取收盘价、开盘价、最高价和最低价数据
close_price = data(:, 1);
open_price = data(:, 2);
high_price = data(:, 3);
low_price = data(:, 4);

% 创建时间序列
t = 1:size(data, 1);

% 绘制三维图
figure;
plot(t, close_price, 'color', '#197AB7','LineWidth',1); % 收盘价
hold on;

xlabel('时间');


%% % 绘制三维图
figure;
plot3(t, 1*ones(size(t)), close_price, 'color', '#197AB7','LineWidth',1); % 收盘价
hold on;
plot3(t, 2*ones(size(t)), open_price, 'color', '#C27C3B','LineWidth',1); % 开盘价
plot3(t, 3*ones(size(t)), high_price, 'Color','#A4D09D','LineWidth',1); % 最高价
plot3(t, 4*ones(size(t)), low_price, 'Color','#84C2AE','LineWidth',1); % 最低价
yticks([1,2,3,4]);
yticklabels({'收盘价', '开盘价', '最高价', '最低价'});
xticks([1,150,300,450,600]);
xticklabels({'2021-9','2022-6','2022-11','2023-6','2024-1'});
xlabel('时间');
zlabel('USD/CNY');
legend('收盘价', '开盘价', '最高价', '最低价');
ztickangle(0);
ax = gca;
ax.XAxis.FontSize = 14; % 设置刻度字体大小


% 更改Y轴刻度标签字体
ax.YAxis.FontSize = 14; % 设置刻度字体大小
ax.ZAxis.FontSize = 14; % 设置刻度字体大小