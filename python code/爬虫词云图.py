# coding=gbk
# -*- coding:uft-8 -*-
# 微博可视化

from wordcloud import WordCloud
import jieba
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


img = Image.open("D:\钱.png")  # 打开遮罩图片
mask = np.array(img)
df = pd.read_excel('D:\汇通财经-外汇-新闻文本.xlsx', engine='openpyxl')
stop = []
kinds = df['新闻文本'].tolist()
words = jieba.cut('/'.join(kinds))
newtxt = ''
stopwords = ["大量","可能","进行","可以","含有","自己","大家","此外","今天","就是","我","你","她","的","是","了","在","也","和","就","都","这","而且","很多","没有"]
for word in words:
    if len(word) > 1 and word not in stop:
        newtxt += word + '/'
wordcloud = WordCloud(background_color='white', mask = mask,width=800, height=600, font_path='msyh.ttc', max_words=200,
                      max_font_size=130,stopwords=stopwords).generate(newtxt)
plt.imshow(wordcloud, interpolation='bilinear')  # 用plt显示图片
plt.axis("off")  # 不显示坐标轴
plt.show()  # 显示图片
wordcloud.to_file('D:\外汇1.png')
