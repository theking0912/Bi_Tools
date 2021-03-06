#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pyhdb
from getaddress.log import gener_log

# get connection
# def conn_db():
#     connection = pyhdb.connect(
#         host="hana-dw.innoventbio.com",
#         port=30015,
#         user="XDSW_JWD",
#         password="XdswJwd2020"
#     )

#     return connection

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
def insertdata(file_path,all_insert_sql):
    all_insert_count = 0
    v_count = 0
    conn = conn_db()
    cursor = conn.cursor()
    for i in range(len(all_insert_sql)):
        v_count = v_count + 1
        print(v_count)
        gener_log.append_log(file_path,all_insert_sql[i] + '\r')
        try:
            print(all_insert_sql[i])
            cursor.execute(all_insert_sql[i])
            insert_count = cursor.rowcount
            all_insert_count = all_insert_count + insert_count
        # 增加主键异常判断
        except pyhdb.exceptions.IntegrityError:
            continue
    cursor.close()
    conn.commit()

    return all_insert_count

# select multiple data
def getMulData(query_sql,query_count):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(query_sql)
    result = cursor.fetchmany(query_count)
    cursor.close()

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

# if __name__ == '__main__':
#     pass