import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

#plt.style.use('_mpl-gallery-nogrid')
pass
file_path = r"D:\z西二\ai\task3\教务通知2.0.csv"
web_data = pd.read_csv(file_path, index_col=0, encoding='gbk')
noti_counts = web_data.groupby('通知人').size().reset_index(name='counts')

plt.figure(figsize=(10, 10))
labels= noti_counts['通知人']
sizes = noti_counts['counts']

plt.rcParams['font.sans-serif'] = ['SimHei']
wedges, texts, autotexts = plt.pie(
    sizes, 
    labels=labels, 
    autopct='%1.1f%%',     
    startangle=90,         
    textprops={'fontsize': 12} 
)

plt.axis('equal')  
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')


plt.show()





plt.figure(figsize=(10, 6))
def cal_total(data,ch):
    if pd.isna(data) or data == "":
        return 0
    try:
        counts = [int(x) for x in str(data).split(ch) if x.isdigit()]
        return sum(counts)
    except ValueError:
        return 0

web_data['该通知人附件总下载次数'] = web_data['附件下载次数'].apply(lambda x: cal_total(x, '|'))

sum_df = web_data.groupby('通知人', as_index=False).agg(
    总下载次数=('该通知人附件总下载次数', 'sum')
)
sum_df.plot.bar(x= '通知人',y = '总下载次数')
plt.show()



plt.figure(figsize=(10, 6))
web_data['日期_时间'] = pd.to_datetime(web_data['日期'], format='%Y/%m/%d', errors='coerce')
web_data['月份'] = web_data['日期_时间'].dt.month
sum_month = web_data.groupby('月份', as_index=False).agg(
    月总下载次数=('该通知人附件总下载次数', 'sum')
)

sum_month.plot.bar(x='月份', y='月总下载次数', figsize=(10, 6), legend=False, color='orange')
plt.show()



plt.figure(figsize=(10, 6))
df2 = pd.DataFrame({
    '通知人': web_data['通知人'],
    '月份': web_data['月份'] 
})
htmp = pd.crosstab(df2['通知人'], df2['月份'])
sns.heatmap(data=htmp, annot=True)
plt.show() 
    