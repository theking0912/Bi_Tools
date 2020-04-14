#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime


def typeof(variate):
    type=None
    if isinstance(variate,int):
        type = "int"
    elif isinstance(variate,str):
        type = "str"
    elif isinstance(variate,float):
        type = "float"
    elif isinstance(variate,list):
        type = "list"
    elif isinstance(variate,tuple):
        type = "tuple"
    elif isinstance(variate,dict):
        type = "dict"
    elif isinstance(variate,set):
        type = "set"
    return type

def getDate():
    nowdate = datetime.datetime.now().strftime('%Y%m%d')
    print(nowdate)

if __name__ == '__main__':
    getDate()