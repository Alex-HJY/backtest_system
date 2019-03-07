# coding: utf-8
"""
Created on 2019/2/25,2:34 PM

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

df = pd.read_csv('month_normal_data.csv', encoding='utf-8-sig', index_col='Date')
df = df.fillna(method='ffill')
df = df.dropna()
# ===========计算因子
df['经济增长'] = (df['工业增加值：当月同比'] + df['PMI'] + df['社会消费品零售总额：当月同比']) / 3
df['通胀'] = (df['CPI：当月同比'] + df['PPI：全部工业品：当月同比']) / 2
df['货币'] = df['M2：同比']
df['信贷'] = (df['国内信贷'] + df['社会融资规模当月值'] + df['社会融资规模同比增长率(%)'] + df['金融机构：各项存款余额同比'] + df['金融机构：各项贷款余额同比']) / 5
df['利率'] = (df['中债国债到期收益率:10年'] + df['中债国开债到期收益率:10年']) / 2
df2 = df[['经济增长', '通胀', '货币', '信贷', '利率']]

# ============计算趋势

month = 5
for each in df2.columns:
    df.ix[0, each + '_趋势'] = '上涨'
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

# =============计算阶段
for i in range(1, df.__len__()):
    if df.ix[i, '经济增长_趋势'] == '下跌' and df.ix[i, '利率_趋势'] == '下跌':
        df.ix[i, '阶段'] = 1
        continue
    if df.ix[i, '经济增长_趋势'] == '上涨' and df.ix[i, '信贷_趋势'] == '上涨':
        df.ix[i, '阶段'] = 2
        continue
    if df.ix[i, '经济增长_趋势'] == '上涨' and df.ix[i, '信贷_趋势'] == '上涨':
        df.ix[i, '阶段'] = 3
        continue
    if df.ix[i, '经济增长_趋势'] == '上涨' and df.ix[i, '通胀_趋势'] == '上涨':
        df.ix[i, '阶段'] = 4
        continue
    if df.ix[i, '通胀_趋势'] == '上涨' :
        df.ix[i, '阶段'] = 5
        continue
    if df.ix[i, '利率_趋势'] == '上涨' and df.ix[i, '利率']>0.5 :
        df.ix[i, '阶段'] = 6
        continue

df.index=pd.DatetimeIndex(df.index)
df2.index=pd.DatetimeIndex(df2.index)
df2.to_csv('five_factor_data.csv', encoding='utf-8-sig')
df['阶段'].plot()
plt.title('经济阶段')
# df2.plot()
# plt.title('指标表现')
plt.show()