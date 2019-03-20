# coding: utf-8
"""
Created on 2019/3/13,4:12 PM

By Alex_HJY
"""
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from dateutil import parser
from datetime import datetime
from dateutil import relativedelta

plt.rcParams['font.sans-serif'] = ['STHeiti']
plt.rcParams['axes.unicode_minus'] = False

df1 = pd.read_excel('指数.xls', encoding='utf-8-sig', index_col='Date')
df1.index = pd.DatetimeIndex(df1.index)
df1 = df1.sort_index()
df1 = df1.fillna(method='ffill')

df2 = pd.read_excel('存款利率.xls', encoding='utf-8-sig', index_col='Date')
df2.index = pd.DatetimeIndex(df2.index)
df2 = df2.sort_index()
df2 = df2.fillna(method='ffill')

df3 = pd.read_csv('000300SH.csv', encoding='utf-8-sig', index_col='Date')
df3.index = pd.DatetimeIndex(df3.index)
df3 = df3.sort_index()
df3 = df3.fillna(method='ffill')

df3 = df3.join(df1)
df3 = df3.join(df2)
df3.fillna(method='ffill', inplace=True)
df3.columns = ['HS300收盘价 ', 'CRB现货指数：综合', '中债综合指数', '定期存款利率：3个月（月）']
df3.to_csv('price_data.csv',encoding='utf-8-sig')