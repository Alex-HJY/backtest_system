# coding: utf-8
"""
Created on 2019/1/23,2:36 PM

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
from dateutil.relativedelta import relativedelta

plt.rcParams['font.sans-serif'] = ['STHeiti']
plt.rcParams['axes.unicode_minus'] = False


def trade_func(df_to_today, today, value, cash, portfolio):
    """
    回测关键函数，可修改，定义每天回测的逻辑

    :param df_to_today: 从起始日期至今的收盘数据
    :param today: date格式,（回测中）当前运行到的日期
    :param value: 资产总值
    :param cash: 当前现金
    :param portfolio: 资产配置，字典，格式为{标的物：购买金额}
    :return: 返回今天的 value, cash, portfolio
    """

    target_dict = {'衰退': ['定期存款利率：3个月（月）'],
                   '复苏': ['HS300收盘价'],
                   '过热': ['CRB现货指数：综合'],
                   '滞涨': ['中债综合指数'], }

    trends = pd.read_csv('trends.csv', encoding='utf-8-sig', index_col='Date')
    trends.index = pd.DatetimeIndex(trends.index)
    now = datetime.now()
    month_now = today + relativedelta(months=1)
    month_now-= relativedelta(days=month_now.day)
    trend = trends.loc[month_now]
    portfolio_new = {}

    for k, v in portfolio.items():
        cash += df_to_today.loc[today, k] * v

    value = cash


    for each in trend.values:
        for target in target_dict[each]:
            portfolio_new[target] = value / df_to_today.loc[today, target]

    for k, v in portfolio_new.items():
        cash -= df_to_today.loc[today, k] * v

    return value, cash, portfolio_new


def get_data():
    df = pd.read_excel('./data/中国宏观数据库.xls', encoding='utf-8-sig', index_col='Date')
    df.index = pd.DatetimeIndex(df.index)
    df = df.sort_index()
    df['CPI&PPI'] = (df['CPI：当月同比'] + df['PPI：全部工业品：当月同比']) / 2
    df = df[['CPI&PPI', '工业增加值：当月同比']]
    df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    df = df.fillna(method='ffill')
    df = df.dropna()
    return df


def get_trends(df=pd.DataFrame(), month=3, delay=0):
    for each in df.columns:
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

    for i in range(1, df.__len__()):
        if df.ix[i, 'CPI&PPI_趋势'] == '下跌' and df.ix[i, '工业增加值：当月同比_趋势'] == '下跌':
            df.ix[i, '阶段'] = '衰退'
            continue
        if df.ix[i, 'CPI&PPI_趋势'] == '下跌' and df.ix[i, '工业增加值：当月同比_趋势'] == '上涨':
            df.ix[i, '阶段'] = '复苏'
            continue
        if df.ix[i, 'CPI&PPI_趋势'] == '上涨' and df.ix[i, '工业增加值：当月同比_趋势'] == '上涨':
            df.ix[i, '阶段'] = '过热'
            continue
        if df.ix[i, 'CPI&PPI_趋势'] == '上涨' and df.ix[i, '工业增加值：当月同比_趋势'] == '下跌':
            df.ix[i, '阶段'] = '滞涨'
            continue

    if delay != 0:
        df['阶段'] = df['阶段'].shift(delay)
    df = df.fillna(method='ffill')
    trend=df['阶段']
    trend=pd.DataFrame(trend)
    trend.columns=['trends']
    trend.to_csv('trends.csv', encoding='utf-8-sig',)
    return trend


if __name__ == '__main__':
    df = get_data()
    trend = get_trends(df, 3, 1)
