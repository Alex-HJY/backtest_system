# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 14:00:03 2018

@author: zhangby
"""

from 张博雅 import basicfunc as bf
import pandas as pd
import numpy as np
#调仓信息类，包括日期，代码，权重
class position:
    def __init__(self,chagdate,stockcode,weight):
        self.chagdate=chagdate
        self.stockcode=stockcode
        self.weight=weight
        
#SelectStockCell=[]
#SelectStockCell.append(position('20180101',('600886.SH','600999.SH'),(0.5,0.5)))
#SelectStockCell.append(position('20180201',('600886.SH','600999.SH'),(0.6,0.4)))
#SelectStockCell.append(position('20180301',('600886.SH','600999.SH'),(0.7,0.3)))
#moneyAmount=1e7

#计算基准涨跌幅函数
def benchmark(begindate,enddate):
    tablename="WIND.AIndexEODPrices"
    condition="S_INFO_WINDCODE='399300.SZ' and TRADE_Dt>='"+begindate+"' and TRADE_Dt<='"+enddate+"'"
    data="DISTINCT TRADE_Dt,S_DQ_PCTCHANGE"
    order="TRADE_Dt"
    benchrtn=bf.get_data_from_DB(data, tablename, condition, order)
    benchrtn=pd.DataFrame(benchrtn)
    benchrtn[1]=benchrtn[1]/100
    return benchrtn
    
      
def backtest(SelectStockCell,moneyAmount):
    print("请输入回测开始时间：")   
    begindate= input()
    print("请输入回测结束时间：")    
    enddate= input()
    benchrtn=benchmark(begindate,enddate)
    
    #回测时间窗内交易日历
    tablename="WIND.AShareCalendar"
    condition="TRADE_DAYS>='"+begindate+"' and TRADE_DAYS<='"+enddate+"'"
    data="DISTINCT TRADE_DAYS"
    order="TRADE_DAYS"
    TRADE_DAYS=bf.get_data_from_DB(data, tablename, condition, order)
    TRADE_DAYS=pd.DataFrame(TRADE_DAYS)
    
    #调仓日期
    change_days=[]
    SelectStockCellInd=[]
    for i in range(0,len(SelectStockCell)):
        change_days.append(SelectStockCell[i].chagdate)
        SelectStockCellInd.append(TRADE_DAYS[(TRADE_DAYS[0]>=SelectStockCell[i].chagdate)].index[0])
    
    #计算每日净值
    nvofportfolio=[]
    for k in range(0,len(TRADE_DAYS)):
        if k<SelectStockCellInd[0]:
            nvofportfolio.append(moneyAmount)
            continue
        if k in SelectStockCellInd:
            if k==SelectStockCellInd[-1]:
                k1=len(TRADE_DAYS)-1
            else:
                k1=SelectStockCellInd[SelectStockCellInd.index(k)+1]
                    
            print(k1)
            stocksweight=SelectStockCell[i].weight
            stockcodestr="'"+SelectStockCell[i].stockcode[0]+"'"
            j=1
            while (j<len(SelectStockCell[i].stockcode)):
                stockcodestr=stockcodestr+",'"+SelectStockCell[i].stockcode[j]+"'"
                j=j+1
            
            tablename="WIND.AShareEODPrices"
            condition="S_INFO_WINDCODE in ("+stockcodestr+") and TRADE_Dt>='"+TRADE_DAYS[0][k]+\
            "' and TRADE_Dt<='"+TRADE_DAYS[0][k1]+"'"           
            data="TRADE_Dt,S_INFO_WINDCODE,S_DQ_OPEN,S_DQ_close,S_DQ_ADJFACTOR"
            order="TRADE_Dt,S_INFO_WINDCODE"
            price=bf.get_data_from_DB(data, tablename, condition, order)
            price=pd.DataFrame(price)
            todayprice=price.loc[price[0]==TRADE_DAYS[0][k],[1,2,3,4]] 
            #每次调仓时计算新持仓
            restmoney=moneyAmount
            shareinhand=[]
            
            adjfac_bench=todayprice[4]
            for l in range(0,len(todayprice[1])):
                shareinhand.append(int(int(moneyAmount*stocksweight[l])/todayprice[2][l]))
                restmoney=restmoney-todayprice[2][l]*shareinhand[l]
                
        todayprice=price.loc[price[0]==TRADE_DAYS[0][k],[1,2,3,4]] 
        todayprice.index = range(len(todayprice))
        adjfac=todayprice[4]
        moneyAmount=np.dot(shareinhand,todayprice[3]*adjfac/adjfac_bench)+restmoney
        nvofportfolio.append(moneyAmount) 
    nvofportfolio=pd.DataFrame(nvofportfolio)
    nvofportfolio.columns=['nv']
    nvofportfolio=TRADE_DAYS.join(nvofportfolio)
    return nvofportfolio,benchrtn


    
#if __name__ == '__main__':
#    result=trybacktest(SelectStockCell,moneyAmount)