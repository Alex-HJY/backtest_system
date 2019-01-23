# coding: utf-8
"""
Created on 2019/1/23,2:11 PM

By Alex_HJY
"""
class A:
    tt=10
    def __init__(self,tt=5):
        self.tt=tt

asa=A(5)
print(asa.tt,A.tt)