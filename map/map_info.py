#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
from time import sleep
from urllib import parse
from urllib import request
from map.utils import hanadb


#  接口地址：https://restapi.amap.com/v3/geocode/regeo?output=json&location=116.310003,39.991957&key=18921641f129198d0c392a95070f4e30
#  接口文档：https://lbs.amap.com/api/webservice/guide/api/georegeo

# 当天日期
nowdate = datetime.datetime.now().strftime('%Y%m%d')

# 高德地图api key
key = '18921641f129198d0c392a95070f4e30'

# 限制数据处理条数，根据API限制规定，高德地图限制6000条/天
process_count = 6

# 生成数据存放表名
table_name = "HANA_DIM.ZT_MAP_ADDR"

# insert sql
insert_sql_be = "INSERT INTO "
insert_sql_mid = " VALUES ('"
insert_sql_en = ")"

# 打卡经纬度数据需要更换为底表数据
lnglat_sql = """
            SELECT CC_ONADDR FROM (
            select distinct a1.YM,a1.CC_ONADDR
              from HANA_DMS.TA_HR_PERSON_PUNCH_BASIC_STAT a1
              left join HANA_DIM.ZT_MAP_ADDR a2
                on a1.CC_ONADDR = a2.LOCATION
             where a2.LOCATION is null
               and (a1.CC_ONADDR != null 
                or a1.CC_ONADDR != '')
             ORDER BY a1.YM DESC)"""

limit_sql = """select count(1) as ins_count from HANA_DIM.ZT_MAP_ADDR WHERE INS_DATE = '""" + nowdate + "'"


# 获取经纬度数据
def getLngLat(lnglat_sql):
    # 获取当日获取条目数
    ins_count = hanadb.getOneData(limit_sql)
    limit_count = process_count - ins_count[0]
    if limit_count > 0:
        result = hanadb.getMulData(lnglat_sql,limit_count)
    else:
        return '','E','高德地图key使用已到上限!'
    return result,'S','Success'

# 获取地址信息
def getAddress():
    # 获取打卡经纬度数据集
    result,process_flag,msg = getLngLat(lnglat_sql)
    if process_flag == 'S' and len(result) > 0:
        data = []

        for n in range(len(result)):
            subdata = ()
            lnglat = str(result[n][0])
            #拼接请求
            url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location='+lnglat+'&key=' + key
            print(url)
            #编码
            newUrl = parse.quote(url, safe="/:=&?#+!$,;'@()*[]")
            # 休眠20 ~ 40ms     QPS 100次/s      1次/10ms
            sleep(0.04)
            body = fetch_data(newUrl)
            if body['status'] == '1':
                # 拼接数据
                api_location = body['regeocode']['addressComponent']['streetNumber']['location']
                location = lnglat
                lng = api_location.split(',')[0]
                lat = api_location.split(',')[1]
                country = body['regeocode']['addressComponent']['country']
                province = body['regeocode']['addressComponent']['province']
                city = body['regeocode']['addressComponent']['city']
                district = body['regeocode']['addressComponent']['district']
                street = body['regeocode']['addressComponent']['streetNumber']['street']
                township = body['regeocode']['addressComponent']['township']

                subdata = (location,lng,lat,country,province,city,district,street,township,nowdate)
                data.append(subdata)
            else:
                continue
    else:
        return '','E','高德地图key使用已到上限'
    return data,'S','Success'

# 生成入库语句
def generinsertsql(table_name,value_dic):
    all_insert_count = 0
    insert_head = insert_sql_be + table_name + insert_sql_mid
    for i in range(len(value_dic)):
        value_part = ''
        for j in range(len(value_dic[i])):
            value_part = value_part + value_dic[i][j] + "','"
        insert_sql = insert_head + value_part[0:-2] + insert_sql_en
        insert_count = hanadb.insertdata(insert_sql)
        all_insert_count = all_insert_count + insert_count

    return all_insert_count,'S','Success'

# 请求api地址
def fetch_data(url):
    req = request.Request(url)  # 请求url（GET请求）
    with request.urlopen(req) as f:     # 打开url请求（如同打开本地文件一样）
        return json.loads(f.read().decode('utf-8'))  # 读数据 并编码同时利用json.loads将json格式数据转换为python对象

if __name__ == "__main__":
    data,process_flag,msg = getAddress()
    if process_flag == 'S' and len(data) > 0:
        all_insert_count,process_flag,msg = generinsertsql(table_name,data)
        print('生成' + all_insert_count + '条数据，执行状态：'+ msg)
    else:
        print(msg)