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
import trade_funcs2

#导入黑体字体，防止无法显示中文
import trade_funcs3

starttime='20120101'
endtime='20181201'

plt.rcParams['font.sans-serif'] = ['STHeiti']
plt.rcParams['axes.unicode_minus'] = False

pricedata = pd.read_csv('./strategies_data/price_data.csv', encoding='utf-8-sig', index_col='Date')
pricedata.index = pd.DatetimeIndex(pricedata.index)

# pricedata.plot()
# plt.show()

bs = backtest_system.backtest_system(price_data=pricedata, benchmark_code='HS300收盘价')
bs.back_test_by_day(trade_func=trade_funcs.trade_func, strategy_name='美林时钟_3_1', start_date=starttime,
                    end_date=endtime)
bs.back_test_by_day(trade_func=trade_funcs2.trade_func2, strategy_name='美林时钟_3_1_var_主观', start_date=starttime,
                    end_date=endtime)
bs.back_test_by_day(trade_func=trade_funcs3.trade_func3, strategy_name='美林时钟_3_1_var_约束', start_date=starttime,
                    end_date=endtime)

print(bs.strategies_indexes)

