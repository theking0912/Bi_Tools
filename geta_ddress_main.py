#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
from getaddress.log import gener_log
from getaddress.utils import hanadb
from getaddress.map import map_info

# 当天日期
nowdatetime = datetime.datetime.now().strftime('%Y%m%d%H')
# 生成数据存放表名
table_name = "HANA_DIM.ZT_MAP_ADDR"

if __name__ == "__main__":
    print('STEP1: 检查目录是否存在')
    # 创建目录
    gener_log.mkdir()

    print('STEP2: 创建日志文件')
    # 创建文件
    file_path = gener_log.mkfile('map_info_address_',nowdatetime)
    gener_log.append_log(file_path,'STEP1 AND STEP2: 检查目录是否存在 AND 创建日志文件\r')

    all_insert_count = 0
    print('STEP3: 通过经纬度解析地址信息，拼接结构化数据，生成INSERT语句')
    gener_log.append_log(file_path,'STEP3: 通过经纬度解析地址信息，拼接结构化数据，生成INSERT语句\r')
    data,process_flag,msg = map_info.getAddress(file_path)

    if process_flag == 'S' and len(data) > 0:
        print('STEP4: 批量生成INSERT语句')
        gener_log.append_log(file_path,'STEP5: 批量生成INSERT语句\r')
        all_insert_sql = map_info.generinsertsql(table_name,data)
        print('STEP5: 执行INSERT语句')
        gener_log.append_log(file_path,'STEP5: 执行INSERT语句\r')
        all_insert_count = hanadb.insertdata(file_path,all_insert_sql)
        gener_log.append_log(file_path,'生成' + str(all_insert_count) + '条数据，执行状态：'+ msg + '\r')
    elif process_flag == 'S' and len(data) == 0:
        msg = '超出api提供限量'
        gener_log.append_log(file_path,msg + '\r')
        print(msg)
    else:
        print(msg)
        gener_log.append_log(file_path,msg + '\r')