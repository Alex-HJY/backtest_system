# coding: utf-8
"""
Created on 2019/1/23,2:11 PM

By Alex_HJY
"""
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from datetime import date
import matplotlib.pyplot as plt
from dateutil import parser

plt.rcParams['font.sans-serif'] = ['STHeiti']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('./data/price_normal.csv', encoding='utf-8-sig', index_col='Date')
df = df.dropna()
df.index = pd.DatetimeIndex(df.index)
df = df.groupby(df.index.strftime('%Y-%m')).mean()
df.index = pd.DatetimeIndex(df.index.map(lambda x: datetime.strptime(x, '%Y-%m')))

month = 4

# =============计算趋势

for each in df.columns:
    df.ix[0, each + '_趋势'] = '上涨'
    if each=='中债':
        month=2
    else:
        month=3
    for i in range(1, df.__len__() - month - 1):

        if df.ix[i, each] == df.ix[i:i + month + 1, each].min() and df.ix[i + month, each] == df.ix[i:i + month + 1,
                                                                                              each].max():
            df.ix[i, each + '_趋势'] = '上涨'
            continue
        if df.ix[i, each] == df.ix[i:i + month + 1, each].max() and df.ix[i + month, each] == df.ix[i:i + month + 1,
                                                                                              each].min():
            df.ix[i, each + '_趋势'] = '下跌'
            continue
        df.ix[i, each + '_趋势'] = df.ix[i - 1, each + '_趋势']

df = df.fillna(method='ffill')

# ===========计算所处经济阶段
for i in range(1, df.__len__()):
    if df.ix[i, '中债_趋势'] == '上涨' and df.ix[i, '中证全指_趋势'] == '下跌' and df.ix[i, 'CRB_趋势'] == '下跌':
        df.ix[i, '阶段'] = 1
        continue
    if df.ix[i, '中债_趋势'] == '上涨' and df.ix[i, '中证全指_趋势'] == '上涨' and df.ix[i, 'CRB_趋势'] == '下跌':
        df.ix[i, '阶段'] = 2
        continue
    if df.ix[i, '中债_趋势'] == '上涨' and df.ix[i, '中证全指_趋势'] == '上涨' and df.ix[i, 'CRB_趋势'] == '上涨':
        df.ix[i, '阶段'] = 3
        continue
    if df.ix[i, '中债_趋势'] == '下跌' and df.ix[i, '中证全指_趋势'] == '上涨' and df.ix[i, 'CRB_趋势'] == '上涨':
        df.ix[i, '阶段'] = 4
        continue
    if df.ix[i, '中债_趋势'] == '下跌' and df.ix[i, '中证全指_趋势'] == '下跌' and df.ix[i, 'CRB_趋势'] == '上涨':
        df.ix[i, '阶段'] = 5
        continue
    if df.ix[i, '中债_趋势'] == '下跌' and df.ix[i, '中证全指_趋势'] == '下跌' and df.ix[i, 'CRB_趋势'] == '下跌':
        df.ix[i, '阶段'] = 6
        continue
print(df)

# df.to_csv('./data/price_trend.csv', encoding='utf-8-sig')

df['阶段'].plot()
plt.title('阶段轮动')
df[['中债','中证全指','CRB']].plot()
plt.title('资产走势')
plt.show()
