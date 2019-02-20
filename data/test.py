# coding: utf-8
"""
Created on 2019/1/23,2:11 PM

By Alex_HJY
"""
import pandas as pd
import numpy as np
from  datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

from datetime import date
from dateutil import parser

def t(x):
    return x[:4]+'/'+x[5:7]

def tt(x):
    x=x-timedelta(days=1)
    return x


df = pd.read_excel('./data/社会融资规模.xls',index_col='Date')
df.index=pd.DatetimeIndex( df.index.map(t))
df.index=df.index.map(tt)
df1 = pd.read_excel('./data/中国宏观数据库.xls',index_col='Date')
df2=pd.read_excel('./data/贷款存款.xls',index_col='Date')
df=df.join(df1)
df=df.join(df2)
print(df)
df.to_csv('./data/month_data.csv')