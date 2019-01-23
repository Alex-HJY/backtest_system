# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 16:09:01 2018

@author: zhangby
@author: huangjy
"""


import cx_Oracle
import os

# 设置ORACLE参数
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
ipaddr = "172.16.109.100"
username = "etf"
password = "etf"
oracle_port = "1521"
oracle_service = "windfs"
conn=cx_Oracle.connect(username+"/"+password+"@"+ipaddr+":"+oracle_port+"/"+oracle_service)
cursor =conn.cursor()


#读取数据函数
def get_data_from_DB(data, tablename, condition, order):
    x=cursor.execute("select "+data+" from "+tablename+" where "+condition+" order by "+order)
    y=x.fetchall()
    return y

