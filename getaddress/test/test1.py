#coding: utf-8
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

#coding: utf-8
import types

#获取字典中的objkey对应的值，适用于字典嵌套
#dict:字典
#objkey:目标key
#default:找不到时返回的默认值
def dict_get(dict, objkey, default):
    tmp = dict
    for k,v in tmp.items():
        if k == objkey:
            return v
        else:
            if type(v) is types.DictType:
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
    return default

#如
ret=dict_get(body2, 'aaa', None)
print(ret)