#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pyhdb

# get connection
def conn_db():
    connection = pyhdb.connect(
    host="172.16.0.62",
    port=34015,
    user="XDSW_BI",
    password="QAH_Bi_2019"
    )

    return connection

# insert data
def insertdata(insert_sql):
    print(insert_sql)
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(insert_sql)
    insert_count = cursor.rowcount
    cursor.close()
    conn.commit()
    conn.close()

    return insert_count

# select multiple data
def getMulData(query_sql,query_count):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(query_sql)
    result = cursor.fetchmany(query_count)
    cursor.close()
    conn.commit()
    conn.close()

    return result

# select one data
def getOneData(query_sql):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(query_sql)
    result = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()

    return result

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


if __name__ == '__main__':
    pass