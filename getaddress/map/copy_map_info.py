#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
from time import sleep
from urllib import parse
from urllib import request
from getaddress.utils import hanadb
from getaddress.log import gener_log


#  接口地址：https://restapi.amap.com/v3/geocode/regeo?output=json&location=116.310003,39.991957&key=18921641f129198d0c392a95070f4e30
#  接口文档：https://lbs.amap.com/api/webservice/guide/api/georegeo

# 高德地图api key
key = '18921641f129198d0c392a95070f4e30'
nowdate = datetime.datetime.now().strftime('%Y%m%d')

# 限制数据处理条数，根据API限制规定，高德地图限制6000条/天
process_count = 6000

# insert sql
insert_sql_be = "INSERT INTO "
insert_sql_mid = " VALUES ('"
insert_sql_en = ");\r"

# 打卡经纬度数据需要更换为底表数据
lnglat_sql = """
                SELECT DISTINCT CC_ONADDR FROM (
            select distinct a1.LDATE,a1.CC_ONADDR
              from "_SYS_BIC"."xdsw.datameta.hr/CA_PERSON_PUNCH_BASIC_STAT" a1
              left join HANA_DIM.ZT_MAP_ADDR a2
                on a1.CC_ONADDR = a2.LOCATION
             where a2.LOCATION is null
               and (a1.CC_ONADDR != null 
                or a1.CC_ONADDR != '')
             ORDER BY a1.LDATE DESC)"""

limit_sql = """select count(1) as ins_count from HANA_DIM.ZT_MAP_ADDR WHERE INS_DATE = '""" + nowdate + "'"

# 获取经纬度数据
def getLngLat(lnglat_sql):
    # 获取当日获取条目数
    ins_count = hanadb.getOneData(limit_sql)
    limit_count = process_count - ins_count[0]
    if limit_count > 0:
        result = hanadb.getMulData(lnglat_sql,limit_count)
        return result,'S','Success'
    else:
        return '','E','高德地图key使用已到上限，明日重置！'

# 获取地址信息
def getAddress(file_path):
    # 获取打卡经纬度数据集
    result,process_flag,msg = getLngLat(lnglat_sql)
    if process_flag == 'S' and len(result) > 0:
        data = []

        for n in range(len(result)):
            subdata = ()
            lnglat = str(result[n][0])
            #拼接请求
            url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location='+lnglat+'&key=' + key
            gener_log.append_log(file_path,url + '\r')
            #编码
            newUrl = parse.quote(url, safe="/:=&?#+!$,;'@()*[]")
            # 休眠20 ~ 40ms     QPS 100次/s      1次/10ms
            sleep(0.04)

            body = fetch_data(newUrl)
            if body['status'] == '1':

                # 拼接数据
                country = get_value(body,'country','NONE')
                province = get_value(body,'province','NONE')
                city = get_value(body,'city','NONE')
                district = get_value(body,'district','NONE')
                township = get_value(body,'township','NONE')
                location = get_value(body,'location','NONE')
                print(location)
                print(hanadb.typeof(location))
                if location != 'NONE':
                    lng = location.split(',')[0]
                    lat = location.split(',')[1]
                else:
                    lng = 'NONE'
                    lat = 'NONE'
                street = get_value(body,'street','NONE')

                subdata = (lnglat,lng,lat,country,province,city,district,street,township,nowdate)
                data.append(subdata)
            else:
                continue
    else:
        return '','E',msg
    return data,'S','Success'

# 生成入库语句
def generinsertsql(table_name,value_dic):
    all_insert_sql = []

    insert_head = insert_sql_be + table_name + insert_sql_mid
    for i in range(len(value_dic)):
        value_part = ''
        for j in range(len(value_dic[i])):
            if value_dic[i][j] == []:
                value_part = value_part + value_dic[i][j-1] + "','"
            else:
                value_part = value_part + value_dic[i][j] + "','"
        insert_sql = insert_head + value_part[0:-2] + insert_sql_en
        all_insert_sql.append(insert_sql)
    return all_insert_sql

# 获取response字段
def get_value(dict,key,value):
    for k,v in dict.items():
        if k == key:
            return v
        else:
            if hanadb.typeof(v) == 'dict':
                if get_value(v,key,value) is not value:
                    return get_value(v,key,value)
    return value

# 请求api地址
def fetch_data(url):
    req = request.Request(url)  # 请求url（GET请求）
    with request.urlopen(req) as f:     # 打开url请求（如同打开本地文件一样）
        return json.loads(f.read().decode('utf-8'))  # 读数据 并编码同时利用json.loads将json格式数据转换为python对象