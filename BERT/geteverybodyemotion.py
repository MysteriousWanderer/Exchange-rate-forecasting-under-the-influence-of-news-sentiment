from transformers import AutoTokenizer, AutoModel
import torch
from torch import nn
import pandas as pd
from tqdm import tqdm
import numpy as np

#模型导入模块
class BERT(nn.Module):
    #将预训练模型导入并且建立一个线性层
    def __init__(self, num_label):
        super().__init__()
        self.bert = AutoModel.from_pretrained("hfl/chinese-bert-wwm-ext")
        self.linear = nn.Linear(768, num_label)
    #输入一个x，通过bert得到输出，然后经过线性层映射到空间上
    def forward(self, X):
        Y = self.bert(**X)
        return self.linear(Y.pooler_output)
#定义了标签的字符串和数字的对应关系
dic={
            2:'positive',
            0:'negative',
            1:'netural'
       }
#将数字转化成对应的字符串
def data_label(X):
    return [dic[i] for i in X]
#iqr去除异常值
def detect_outliers(data):
    quartile_1 = np.percentile(data, 25)
    quartile_3 = np.percentile(data, 75)
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - 1.5 * iqr
    upper_bound = quartile_3 + 1.5 * iqr
    outliers_indices = np.where((data < lower_bound) | (data > upper_bound))
    return outliers_indices
#载入环境文件
model = torch.load("./model/modelforsentiment.pkl")
#设置成评估模式，这样避免参数更新
model.eval()

#初始化了一个BERT的tokenizer，用于将文本转换为BERT模型的输入格式。（将数据规格化）
modelcheckpoint="/root/project_code/model/hfl/chinese-bert-wwm-ext/"
tokenizer = AutoTokenizer.from_pretrained(modelcheckpoint)
#读取数据

df = pd.read_csv("./emotional_news.csv",encoding="utf-8",usecols=("time","summary"))
df1= pd.read_csv("./emotional_news.csv",encoding="utf-8",usecols=("time","summary"))
#将新闻摘要一列转化程列表
batch = df['summary'].to_list()

prediction = []
labels = []

#tqdm生成进度用（可视化）
for i in tqdm(range(0,len(batch),32)):
    #每次取一个batch_size=32的batch，如果最后一个不足32，直接取所有剩余样本
    if len(batch)-i<=32:
        e = batch[i:len(batch)]
    else:
        e = batch[i:i+32]

    input_data = tokenizer(e,padding=True,return_tensors='pt').to('cuda')
    #模型生成结果
    output_data = model(input_data)
    # 将output_data转换为CPU上的Tensor
    prediction += output_data.detach().cpu().numpy().tolist()
    for row in output_data.detach().cpu().numpy().tolist():
        max_value = max(row)
        max_index = row.index(max_value)
        labels.append(data_label([max_index])[0])


#把数据做成新的表格
#将三列情绪向量加上对应的列表构成一个新的表格，然后和原有的数据表格合并
df = pd.concat((df, pd.DataFrame(data=prediction,columns=('negative','neutral','positive'))),axis=1,ignore_index=True)
df = pd.concat((df, pd.DataFrame(data=labels,columns=['label'])),axis=1,ignore_index=True)
#把列标进行更新
df.columns=("date","summary","nagetive","neutral","positive",'lable')
print(df)

#把上方合并后的excel文件保存
df.to_csv(r'/root/result(dat-new-emo).csv', index=False, encoding='UTF-8')


#按照日期进行分组，统计某一天的情感向量
df1= df1.groupby('date')
data = []
for t,d in df1:
    d = d.to_numpy()
    metric= np.array([0,0,0])
    for e in d:
        metric = metric + e[2:]
    data.append([t,metric[0],metric[1],metric[2]])

data = pd.DataFrame(data,columns=['date', 'negative' , 'netural', 'positive'])
data.to_csv(r'/root/result(dat-emo).csv', index=False)




