#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os

dirPath = 'E:/py/map/getaddress/logs/'

# 创建路径
def mkdir():
    if(os.path.exists(dirPath)):
        pass
        print("目录"+dirPath+"已经存在")
    else:
        os.mkdir(dirPath)
        print("创建目录"+dirPath)

# 创建日志文件
def mkfile(log_type,file_name):
    file_path = dirPath + log_type + file_name
    print("file_path： "+ file_path)
    file = open(file_path,"w+")#(w+: 开头开始编辑，如不存在则创建)
    file.write(file_path)
    file.closed

    return file_path

# 删除7天的日志文件
def removefile(removedate):
    os.remove();

# 追加日志
def append_log(file_path,log_detail):
    file = open(file_path, "a+")  # （a+: 用户追加写入）
    file.write(log_detail)
    file.closed
