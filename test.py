# coding: utf-8
"""
Created on 2019/3/13,11:14 AM

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
import backtest_system

import trade_funcs

#导入黑体字体，防止无法显示中文
plt.rcParams['font.sans-serif'] = ['STHeiti']
plt.rcParams['axes.unicode_minus'] = False



pricedata = pd.read_csv('./strategies_data/price_data.csv', encoding='utf-8-sig', index_col='Date')
pricedata.index = pd.DatetimeIndex(pricedata.index)




bs = backtest_system.backtest_system(price_data=pricedata, benchmark_code='HS300收盘价')
bs.back_test_by_day(trade_func=trade_funcs.trade_func, strategy_name='美林时钟_3_1', start_date='20120101',
                    end_date='20180101')
print(bs.strategies_indexes)
