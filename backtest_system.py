# coding: utf-8
"""
Created on 2019/1/23,2:11 PM

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


class backtest_system:
    def __init__(self, price_data=pd.DataFrame(), benchmark_code='', initial_money=1000000, save_dir='', start_date='', end_date=''):
        """
        构建回测系统时的初始化函数

        :param price_data: 股票价格数据
        :param bench_mark: 基准标的物（代码）
        :param initial_money: 起始现金
        :param save_dir: 储存目录
        :return backtest_result: 回测结果,DataFrame格式
        """
        self.benchmark_code = benchmark_code
        self.start_date=parser.parse(start_date)
        self.end_date= parser.parse(end_date)
        self.strategies_data = {}  # 存放本系统中运行的策略对应的回测数据
        self.strategies_indexes = {}  # 存放本系统中运行的策略对应的回测指标
        self.price_data = deepcopy(price_data)
        self.price_data.index=pd.DatetimeIndex(self.price_data.index)
        self.benchmark_value=self.cal_benchmark_value(benchmark_code)
        self.init_money = initial_money
        self.save_dir = save_dir
        self.backtest_result = pd.DataFrame()
        self.today = datetime.today()

    def order_by_share(self, target_stock, target_share):
        pass

    def order_by_money(self, target_stock, target_money):
        pass

    def cal_benchmark_value(self, benchmark_code):
        benchmark_price=self.price_data[benchmark_code]
        benchmark_price=benchmark_price[self.start_date:self.end_date]
        share=benchmark_price.iloc[0]/self.init_money
        return benchmark_price*share

    # =====================需要重写


    def back_test_by_day(self, strategy_name='', trade_func='', before_trade_func='',
                         after_trade_func='', show=True):
        """

        :param show: 是否画图
        :param before_trade_func: 交易后执行函数
        :param after_trade_func: 交易前执行函数
        :param strategy_name: 策略名称
        :param trade_func: 交易函数，函数参数为df_to_today, today,  value, cash, portfolio
        :param start_date: 起始日期
        :param end_date: 结束日期
        :return: df 包含策略的 CASH,MONEY,PORTFOLIO
        """

        # 设定初始参数
        price_data = self.price_data
        value = self.init_money
        cash = self.init_money
        portfolio = {}
        df_to_today = pd.DataFrame()
        backtest_result = self.backtest_result
        one_day = timedelta(days=1)
        start_date = self.start_date
        end_date = self.end_date
        today = start_date
        bench_mark = self.benchmark_code

        backtest_result.index=price_data.index
        backtest_result['value'] = ''
        backtest_result['cash'] = ''
        backtest_result['portfolio'] = ''

        # 按天回测
        while today < end_date:
            if today in price_data.index:
                df_to_today = df_to_today.append(price_data.loc[today])
                value, cash, portfolio = trade_func(df_to_today, today, value, cash, portfolio)
                backtest_result.loc[today, 'value'] = value
                backtest_result.loc[today, 'cash'] = cash
                backtest_result.loc[today, 'portfolio'] = portfolio
            today = today + one_day

        self.strategies_data[strategy_name] = backtest_result
        self.strategies_indexes[strategy_name]=self.calculate_indexes([strategy_name])


        if show:
            self.show([strategy_name])

        if self.save_dir != '':
            backtest_result.to_csv(self.save_dir + strategy_name + '.csv', encoding='utf-8-sig')

        return backtest_result




    def show(self, strategies_name=[]):
        """

        :param strategies_name:策略名称，数组
        :return:无
        """
        plt.plot(self.benchmark_value.index, self.benchmark_value, label=self.benchmark_code)
        for strategy in strategies_name:
            df=self.strategies_data[strategy]
            plt.plot(df.index, df['money'], label=strategy)
        plt.legend()
        plt.show()
        return None



#================需要重写
    def calculate_indexes(self,strategies_name=[]):
        """

        :param strategies_name: 策略名称，数组
        :return: 无
        """
        pass

    # def get_indexes(self, df, strategies_name=[]):
    #     indexes = pd.DataFrame()
    #     for name in strategies_name:
    #         # 年化收益率
    #         r = (df.iloc[-1][name] * 1.0 / df.iloc[0][name]) ** (250 * 1.0 / df[name].__len__()) - 1
    #
    #         # 回撤
    #         d = 0
    #         t = df.iloc[0][name]
    #         for i in range(1, df[name].__len__()):
    #             t = max(t, df.iloc[i][name] * 1.0)
    #             d = max(d, 1 - df.iloc[i][name] * 1.0 / t)
    #         # sharp
    #         rt = []
    #         for i in range(df.index[0].year, df.index[-1].year):
    #             rt.append((df[str(i)].ix[-1, name] - df[str(i)].ix[0, name]) * 1.0 / df[str(i)].ix[0, name] - 1)
    #         rt = np.array(rt)
    #         rt = rt * 100
    #         sigma = rt.std()
    #         sharp = (r - 0.028) * 100 / sigma
    #
    #         # 胜率
    #         win = df[(df[name] - df[name].shift(-1)) > 0][name].count() * 1.0 / df.__len__()
    #
    #         # beta alpha
    #         df[name + '_rtn'] = (df[name] - df[name].shift(-1)) / df[name] * 100
    #
    #         df[self.bench_mark + '_rtn'] = (df[self.bench_mark + '_money'] - df[self.bench_mark + '_money'].shift(-1)) / \
    #                                        df[self.bench_mark + '_money'] * 100
    #         df[name + '_rtn'] = df[name + '_rtn'].map(float)
    #         df[self.bench_mark + '_rtn'] = df[self.bench_mark + '_rtn'].map(float)
    #         beta = df[name + '_rtn'][:-1].cov(df[self.bench_mark + '_rtn'][:-1]) / df[self.bench_mark + '_rtn'][
    #                                                                                :-1].var()
    #         alpha = (r - 0.0284) - beta * (
    #                 ((df.iloc[-1][self.bench_mark + '_money'] * 1.0 / df.iloc[0][self.bench_mark + '_money']) ** (
    #                         250 * 1.0 / df.__len__()) - 1) - 0.0284)
    #
    #         index = {'策略收益': [str(((df.iloc[-1][name] * 1.0 / df.iloc[0][name])) * 100)],
    #                  '基准收益': [str(((df.iloc[-1][self.bench_mark + '_money'] * 1.0 / df.iloc[0][
    #                      self.bench_mark + '_money'])) * 100)],
    #
    #                  '策略收益率': [str(r * 100) + '%'],
    #                  '回撤': [str(d * 100) + '%'],
    #                  'sharp': [str(sharp)],
    #                  '上涨率': [str(win)],
    #                  'alpha': [alpha],
    #                  'beta': [beta]}
    #         index = pd.DataFrame(index)
    #     indexes = indexes.append(index)
    #     return indexes
