# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 17:30:49 2018

@author: zhangby
"""

import backtest as bt
import basicfunc as bf
import pandas as pd
import numpy as np

stockpool = '399330.SZ'
changedt = ['20180101', '20180201', '20180301']


def preclose(stockcodestr, TRADE_DAYS):
    stockcell = {'stockcode': stockcodestr, 'weight': 2}
    return stockcell


def selectstock(stockpool, changedt, factor):
    SelectStockCell = []

    for i in range(0, len(changedt)):
        tablename = "WIND.AShareCalendar"
        condition = "TRADE_DAYS>='" + changedt[i] + "'"
        data = "min(TRADE_DAYS)"
        order = "TRADE_DAYS"
        TRADE_DAYS = bf.get_data_from_DB(data, tablename, condition, order)
        TRADE_DAYS = pd.DataFrame(TRADE_DAYS)

        tablename = 'WIND.AIndexMembers'
        condition = "S_INFO_WINDCODE='" + stockpool + "' and ((S_CON_INDATE<=" + TRADE_DAYS[0][0] \
                    + " and S_CON_OUTDATE>=" + TRADE_DAYS[0][0] + ") or (S_CON_INDATE<=" + TRADE_DAYS[0][0]\
                    + " and CUR_SIGN=1))"
        data = 'S_CON_WINDCODE'
        order = 'S_CON_WINDCODE'
        stockcode = bf.get_data_from_DB(data, tablename, condition, order)
        stockcode = pd.DataFrame(stockcode)

        j = 1
        stockcodestr = "'" + stockcode[0][0] + "'"
        while (j < len(stockcode[0])):
            stockcodestr = stockcodestr + ",'" + stockcode[0][j] + "'"
            j = j + 1

        stockcell = factor(stockcodestr, TRADE_DAYS)
        SelectStockCell.append(bt.position(changedt[i], stockcell['stockcode'], stockcell['weight']))
    return SelectStockCell


if __name__ == '__main__':
    result = selectstock(stockpool, changedt, preclose)
