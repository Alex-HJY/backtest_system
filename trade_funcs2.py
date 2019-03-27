# coding: utf-8
"""
Created on 2019/3/20,4:44 PM

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
from decimal import Decimal

plt.rcParams['font.sans-serif'] = ['STHeiti']
plt.rcParams['axes.unicode_minus'] = False
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.optimize as sco


def trade_func2(df_to_today, today, value, cash, portfolio):
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
    month_last = today - relativedelta(days=today.day)
    month_now = today + relativedelta(months=1)
    month_now -= relativedelta(days=month_now.day)
    trend = trends.loc[month_now].values[0]
    trend_last = trends.loc[month_last].values[0]

    portfolio_new = {}

    for k, v in portfolio.items():
        cash += df_to_today.loc[today, k] * v

    value = cash

    # print(trend)
    # print(trend_last)

    if (trend != trend_last) and today.day == 1:
        weights = calc_mv(df_to_today, 4, 100)
        for k, v in weights.items():
            if k == target_dict[trend][0]:
                weights[k] = weights[k] + 0.3
            weights[k] = weights[k]/1.3
        print(weights)
        for k, v in weights.items():
            portfolio_new[k] = value * weights[k] / df_to_today.loc[today, k]

        print(portfolio_new, '???')
    else:
        portfolio_new = portfolio

    for k, v in portfolio_new.items():
        cash -= df_to_today.loc[today, k] * v
    print(value, cash, portfolio_new)
    return value, cash, portfolio_new


def calc_mv(df, n_assets=4, n_obs=500):
    def portfolio(weights):
        weights = np.array(weights)
        # print(returns_means)
        port_returns = np.dot(weights.T, returns_means)
        port_variance = np.sqrt(np.dot(weights.T, np.dot(np.cov(returns), weights)))

        return np.array([port_returns, port_variance, port_returns / port_variance])

    def min_sharpe(weights):
        return -portfolio(weights)[2]

    def min_variance(weights):
        return portfolio(weights)[1]

    returns = df[['定期存款利率：3个月（月）', 'HS300收盘价', 'CRB现货指数：综合', '中债综合指数']]
    returns = returns.iloc[-n_obs:, :]
    # print(returns)
    returns = returns.values.T
    cov = np.cov(returns)
    returns_means = np.mean(returns, axis=1)
    port_returns, port_variance = [], []

    for i in range(400):
        weights = np.random.rand(n_assets)
        weights /= sum(weights)

        port_returns.append(portfolio(weights)[0])
        port_variance.append(portfolio(weights)[1])

    port_returns = np.array(port_returns)
    port_variance = np.array(port_variance)

    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    bnds = tuple((0, 0.5) for x in range(n_assets))

    optv = sco.minimize(min_variance, n_assets * [1. / n_assets, ], method='SLSQP',
                        bounds=bnds, constraints=cons)

    opts = sco.minimize(min_sharpe, n_assets * [1. / n_assets, ], method='SLSQP',
                        bounds=bnds, constraints=cons)

    target_returns = np.linspace(portfolio(optv['x'])[0], portfolio(optv['x'])[0] + 0.03, 80)

    target_variance = []

    for tar in target_returns:
        cons2 = ({'type': 'eq', 'fun': lambda x: portfolio(x)[0] - tar},
                 {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        res = sco.minimize(min_variance, n_assets * [1. / n_assets, ], method='SLSQP',
                           bounds=bnds, constraints=cons2)
        target_variance.append(res['fun'])

    target_variance = np.array(target_variance)
    #
    # plt.xlabel('std')
    # plt.ylabel('mean')
    # plt.title('Mean and std-dev of returns')
    #
    # plt.plot(port_variance, port_returns, 'o', markersize=3)
    # plt.plot(target_variance, target_returns, 'y-', markersize=15)
    #
    # plt.plot(portfolio(optv['x'])[1], portfolio(optv['x'])[0], 'y*', markersize=20.0)
    # plt.plot(portfolio(opts['x'])[1], portfolio(opts['x'])[0], 'r*', markersize=20.0)
    # plt.show()

    weight_dict = {'定期存款利率：3个月（月）': optv['x'][0],
                   'HS300收盘价': optv['x'][1],
                   'CRB现货指数：综合': optv['x'][2],
                   '中债综合指数': optv['x'][3], }
    print(weight_dict)
    return weight_dict
