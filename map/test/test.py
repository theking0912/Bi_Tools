#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os

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


if __name__ == '__main__':
    mkdir()