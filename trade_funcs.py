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
import trade_funcs as tf

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

    return value,cash,portfolio