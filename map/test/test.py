#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os

import pyhdb
from map.utils import hanadb

dirPath = 'C:/Users/37646/IdeaProjects/Bi_Tools/map/log/'
nowdate = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def generinsertsql():
    value_dic = [('116.290137,39.923261', '116.289629', '39.9233011', '中国', '北京市', '北京市', '海淀区', '阜成路', '八里庄街道', '20200414')]
    for i in range(len(value_dic)):
        value_part = ''
        print(value_dic[i])
        for j in range(len(value_dic[i])):
            if value_dic[i][j] == []:
                value_part = value_part + value_dic[i][j-1] + "','"
            else:
                value_part = value_part + value_dic[i][j] + "','"
            print(value_part)

# 创建log
def mkdir():
    if(os.path.exists(dirPath)):
        pass
        print("目录"+dirPath+"已经存在")
    else:
        os.mkdir(dirPath)
        print("创建目录"+dirPath)
    file_path = dirPath + nowdate
    print("file_path： "+ file_path)
    file = open(file_path,"w+")#(w+: 开头开始编辑，如不存在则创建)
    file.write("hello world!")
    file.closed

    file = open(file_path, "a+")  # （a+: 用户追加写入）
    file.write("hello world!")
    file.closed

def conn_db():
    connection = pyhdb.connect(
        host="172.16.0.62",
        port=34015,
        user="XDSW_BI",
        password="QAH_Bi_2019"
    )

    return connection

all_insert_sql = ["""INSERT INTO HANA_DIM.ZT_MAP_ADDR VALUES ('120.74028483072917,31.254676649305555','120.74021','31.2548331','中国','江苏省','苏州市','苏州工业园区','裕新路','苏州工业园区直属镇','20200415');
""","""INSERT INTO HANA_DIM.ZT_MAP_ADDR VALUES ('120.738545,31.256886','120.737911','31.2575139','中国','江苏省','苏州市','苏州工业园区','若水路','苏州工业园区直属镇','20200415');
"""]

# insert data
def insertdata(all_insert_sql):
    all_insert_count = 0
    conn = conn_db()
    cursor = conn.cursor()
    for i in range(len(all_insert_sql)):
        print(all_insert_sql[i])
        try:
            cursor.execute(all_insert_sql[i])
            insert_count = cursor.rowcount
            all_insert_count = all_insert_count + insert_count
        except pyhdb.exceptions.IntegrityError:
            continue
    cursor.close()
    conn.commit()

    return all_insert_count

if __name__ == '__main__':
    insertdata(all_insert_sql)