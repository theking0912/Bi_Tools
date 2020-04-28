
#! /usr/bin/env python
# -*- coding: utf-8 -*-
''' 解压一个.zip文件或一个目录下的所有.zip文件到指定目录。
    
    运行方法： 
    格式：
        python unzip.py "source_dir" "dest_dir" password
    参数说明：
        source_dir和dest_dir既可以绝对路径也可以为相对路径。用""将它们括起为了防止路径中出现空格。
        source_dir和dest_dir的缺省值表示当前目录。
        password缺省表示压缩文件未加密。
    注意：
        1. 若目录太长，可以将上述语句直接写入.bat脚本，然后运行脚本。
        2. 密码的编码格式为“utf-8”，且不支持WinRAR中zip格式的默认加密算法--CBC模式下的AES-256。
           若想要WinRAR加密压缩的.zip文件能用本程序顺利解压，请在加密压缩时勾选“ZIP传统加密”。     
'''

import sys, os, zipfile

def unzip_single(src_file, dest_dir, password):
    ''' 解压单个文件到目标文件夹。
    '''
    if password:
        password = password.encode()
        print(password)
    zf = zipfile.ZipFile(src_file)
    try:
        zf.extractall(path=dest_dir, pwd=password)
    except RuntimeError as e:
        print(e)
    zf.close()

def unzip_all(source_dir, dest_dir, password):
    if not os.path.isdir(source_dir):    # 如果是单一文件
        unzip_single(source_dir, dest_dir, password)
    else:
        it = os.scandir(source_dir)
        for entry in it:
            if entry.is_file() and os.path.splitext(entry.name)[1]=='.zip' :
                unzip_single(entry.path, dest_dir, password)
    
if __name__ == "__main__":
    
    # 获取源路径和目标路径
    source_dir = os.getcwd()+'\\unzip\\zipfile\\'
    dest_dir = os.getcwd()+'\\unzip\\unzipfile\\'

    password = 'Innovent2020'
    # password = '123qwe'
    if len(sys.argv) == 2: # 指定了压缩文件所在路径
        source_dir = sys.argv[1]
    if len(sys.argv) == 3: # 压缩文件所在和解压到路径均指定
        source_dir, dest_dir = os.path.abspath(sys.argv[1].strip('"')), os.path.abspath(sys.argv[2].strip('"'))
    if len(sys.argv) == 4: # 还指定了密码
        source_dir, dest_dir, password =  os.path.abspath(sys.argv[1].strip('"')), os.path.abspath(sys.argv[2].strip('"')), sys.argv[3]
    if len(sys.argv) > 4:
        print('过多的参数，可能是路径中有空白字符，请用""将路径括起。')
        exit()
    
    print("源目录:", source_dir)
    print("解压到:", dest_dir)
    print("解压密码:", password)
    
    # 判断源路径是否合法
    if not os.path.exists(source_dir):
        print("压缩文件或压缩文件所在路径不存在！")
        exit()
    if not os.path.isdir(source_dir) and not zipfile.is_zipfile(source_dir):
        print("指定的源文件不是一个合法的.zip文件！")
        exit()
    
    # 如果解压到的路径不存在，则创建     
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    unzip_all(source_dir, dest_dir, password)


# # import pandas as pd
# # zf=zipfile.ZipFile("C:/Users/37646/IdeaProjects/Bi_Tools/unzip/zipfile/ITAPI1_TEST02.zip")
# # print(zf.namelist())
# # zf.extractall(path="C:/Users/37646/IdeaProjects/Bi_Tools/unzip/zipfile/ITAPI1_TEST02.zip", pwd='Innovent2020')
# # f=zf.open('1.xlsx',mode='r',pwd='Innovent2020'.encode('utf-8'))
# # df=pd.read_excel(f)
# # print(df)
# # zf.close()