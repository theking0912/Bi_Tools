#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import json
from urllib import request

import pyhdb
from getaddress.utils import hanadb

dirPath = 'C:/Users/37646/IdeaProjects/Bi_Tools/map/log/'
nowdate = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

body = {
    "status": "1",
    "info": "OK",
    "infocode": "10000",
    "regeocode": {
        "formatted_address": [ ],
        "addressComponent": {
            "country": [ ],
            "province": [ ],
            "city": [ ],
            "citycode": [ ],
            "district": [ ],
            "adcode": [ ],
            "township": [ ],
            "towncode": [ ]
        },
        "pois": [ ],
        "roads": [ ],
        "roadinters": [ ],
        "aois": [ ]
    }
}

body2 = {
    "status": "1",
    "regeocode": {
        "addressComponent": {
            "city": "苏州市",
            "province": "江苏省",
            "adcode": "320571",
            "district": "苏州工业园区",
            "towncode": "320571199000",
            "streetNumber": {
                "number": "388号E幢",
                "location": "120.739409,31.25912",
                "direction": "北",
                "distance": "134.066",
                "street": "若水路"
            },
            "country": "中国",
            "township": "苏州工业园区直属镇",
            "businessAreas": [
                [ ]
            ],
            "building": {
                "name": [ ],
                "type": [ ]
            },
            "neighborhood": {
                "name": [ ],
                "type": [ ]
            },
            "citycode": "0512"
        },
        "formatted_address": "江苏省苏州市苏州工业园区苏州工业园区直属镇东平街苏州生物纳米科技园"
    },
    "info": "OK",
    "infocode": "10000"
}

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

def asd():
    body = {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "regeocode": {
            "formatted_address": [ ],
            "addressComponent": {
                "country": [ ],
                "province": [ ],
                "city": [ ],
                "citycode": [ ],
                "district": [ ],
                "adcode": [ ],
                "township": [ ],
                "towncode": [ ]
            },
            "pois": [ ],
            "roads": [ ],
            "roadinters": [ ],
            "aois": [ ]
        }
    }
    print('1')
    print(hanadb.typeof(body))
    if body['status'] == '1':
        # 拼接数据
        addressComponent = body['regeocode']['addressComponent']
        for k,v in addressComponent.items():
            if k == 'country' and addressComponent['country'] != '':
                country = addressComponent['country']
            elif k == 'c' and addressComponent['province'] != '':
                province = addressComponent['province']
            elif k == 'city':
                if addressComponent['city'] != '':
                    city = addressComponent['province']
                else:
                    city = addressComponent['city']
            elif k == 'district':
                district = addressComponent['district']
            elif k == 'township':
                township = addressComponent['township']
            else:
                streetNumber = addressComponent['streetNumber']
                for k2,v2 in streetNumber.items():
                    if k2 == 'location':
                        api_location = streetNumber['location']
                        lng = api_location.split(',')[0]
                        lat = api_location.split(',')[1]
                    elif k2 == 'street':
                        street = streetNumber['street']

    else:
        print('111111')

def aaa():

    # print(hanadb.typeof(body))
    # if 'country' in body2:
    #     print(body2.get('regeocode').get('addressComponent').get('country'))
    # if 'province' in body2:
    #     print(body2.get('regeocode').get('addressComponent').get('province'))
    # if 'city' in body2:
    #     print(body2.get('regeocode').get('addressComponent').get('city'))
    # if 'district' in body2:
    #     print(body2.get('regeocode').get('addressComponent').get('district'))
    # if 'township' in body2:
    #     print(body2.get('regeocode').get('addressComponent').get('township'))
    # if 'location' in body2:
    #     print(body2.get('regeocode').get('addressComponent').get('streetNumber').get('location').split(',')[0])
    #     print(body2.get('regeocode').get('addressComponent').get('streetNumber').get('location').split(',')[1])
    # if 'street' in body2:
    #     print(body2.get('regeocode').get('addressComponent').get('streetNumber').get('street'))
    #

    print(body2.get('regeocode').get('addressComponent').get('country'))
    print(body2.get('regeocode').get('addressComponent').get('province'))
    print(body2.get('regeocode').get('addressComponent').get('city'))
    print(body2.get('regeocode').get('addressComponent').get('district'))
    print(body2.get('regeocode').get('addressComponent').get('township'))
    print(body2.get('regeocode').get('addressComponent').get('streetNumber').get('location').split(',')[0])
    print(body2.get('regeocode').get('addressComponent').get('streetNumber').get('location').split(',')[1])
    print(body2.get('regeocode').get('addressComponent').get('streetNumber').get('street'))

    print('----------')

def bbb(body,addr_dict):
    for k,v in body.items():
        if hanadb.typeof(v) == 'dict':
            print(addr_dict)
            return bbb(v,addr_dict)
        else:
            if k == 'country':
                addr_dict[k] = v
            elif k == 'province':
                addr_dict[k] = v
            elif k == 'city':
                addr_dict[k] = v
            elif k == 'district':
                addr_dict[k] = v
            elif k == 'township':
                addr_dict[k] = v
            elif k == 'location':
                addr_dict[k] = v
            elif k == 'street':
                addr_dict[k] = v

def xxx(body):
    addr_list = []
    for k,v in body.items():
        if hanadb.typeof(v) == 'dict':
            xxx(v)
        elif hanadb.typeof(v) == 'str':
            print(k,v)
            print('--------------')
        else:
            continue


# def ccc(body,list_key):
#     for k,v in body.items():
#         if hanadb.typeof(v) == 'dict':
#             list_key.append({'level':0,'value':k,'ifdict':1})
#         else:
#             list_key.append({'level':0,'value':k,'ifdict':0})
#     return list_key
#
# def get_key(body):
#     list_key = [{'level': -1, 'value': '0', 'ifdict': 1}]
#     for i in list_key:
#         if i['ifdict'] == 1:
#             if i['value'] == '0':
#                 dicts = body
#             else:
#                 dicts = body[]
#                 a= ccc(dicts,list_key)
#                 print(a)

def get_dict(dict,key,value):
    for k,v in dict.items():
        if k == key:
            return v
        else:
            if hanadb.typeof(v) == 'dict':
                if get_dict(v,key,value) is not value:
                    return get_dict(v,key,value)
    return value

if __name__ == '__main__':
    print(get_dict(body2,'country','NONE'))
    print(get_dict(body2,'province','NONE'))
    print(get_dict(body2,'city','NONE'))
    print(get_dict(body2,'district','NONE'))
    print(get_dict(body2,'township','NONE'))
    print(get_dict(body2,'location','NONE').split(',')[0])
    print(get_dict(body2,'location','NONE').split(',')[1])
    print(get_dict(body2,'street','NONE'))
    # addr_dict = {}
    # print(addr_dict)
    # addr_dict = bbb(body2,addr_dict)
    # print(addr_dict)

    # a = xxx(body2)
    # print(a)
