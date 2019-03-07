# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 14:00:03 2018

@author: zhangby
"""

from 张博雅 import backtest as bt
import numpy as np
import matplotlib.pyplot as pl
        
SelectStockCell=[]
SelectStockCell.append(bt.position('20180101',('600886.SH','600999.SH'),(0.5,0.5)))
SelectStockCell.append(bt.position('20180201',('600886.SH','600999.SH'),(0.6,0.4)))
SelectStockCell.append(bt.position('20180301',('600886.SH','600999.SH'),(0.7,0.3)))
moneyAmount=1e7
      
def testIndex(SelectStockCell,moneyAmount):
    [nvofportfolio,benchrtn]=bt.backtest(SelectStockCell,moneyAmount)
    nvofportfolio['rtnrate']=nvofportfolio['nv']/nvofportfolio['nv'].shift(1)-1
    nvofportfolio['rtnrate'][0]=nvofportfolio['nv'][0]/moneyAmount-1
    nvofportfolio['cumulrtn']=nvofportfolio['nv']/moneyAmount
    nvofportfolio['benchrtn']=benchrtn[1]
    nvofportfolio['ExcessReturn']=nvofportfolio['rtnrate']-benchrtn[1]
    nvofportfolio['CumulExcRtn']=(nvofportfolio['ExcessReturn']+1).cumprod()
    nvofportfolio['CumulbenchReturn']=(nvofportfolio['benchrtn']+1).cumprod()
    
    datenum=len(nvofportfolio)
    annualrtn=nvofportfolio['cumulrtn'][datenum-1]**(250/(datenum))-1
    returnstd=np.std(nvofportfolio['rtnrate'])
    annualstd=returnstd*np.sqrt(250/(datenum))
    riskfree=0.033
    sharperatio=(annualrtn-riskfree)/annualstd
    drawback=max(1-nvofportfolio['nv']/nvofportfolio['nv'].cummax())
    #winrate=sum(nvofportfolio.rtnrate>0)/(datenum)
    
    AnnualExcRtn=nvofportfolio['CumulExcRtn'][datenum-1]**(250/(datenum))-1
    
    ExcRtnStd=np.std(nvofportfolio['ExcessReturn'])
    annualExcStd=ExcRtnStd*np.sqrt(250/(datenum))
    IR=AnnualExcRtn/annualExcStd
    excwinrate=sum(nvofportfolio.ExcessReturn>0)/(datenum)
    drawback=max(1-nvofportfolio['CumulExcRtn']/nvofportfolio['CumulExcRtn'].cummax())
    testIndex={'交易日天数':datenum,'年化收益率':annualrtn,'年化标准差':annualstd,\
              'Sharpe比':sharperatio,'年化超额收益':AnnualExcRtn,'年化超额标准差':annualExcStd,\
              'IR值':IR,'超额收益日胜率':excwinrate,'最大回撤':drawback}
    pl.plot(nvofportfolio[0],nvofportfolio['cumulrtn'])
    pl.plot(nvofportfolio[0],nvofportfolio['CumulExcRtn'])
    pl.plot(nvofportfolio[0],nvofportfolio['CumulbenchReturn'])
    pl.xticks(rotation=90)
    pl.show()

    return nvofportfolio,testIndex


    
if __name__ == '__main__':
    [nvofportfolio,testIndex]=testIndex(SelectStockCell,moneyAmount)