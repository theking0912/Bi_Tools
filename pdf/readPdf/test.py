# -*- coding: utf-8 -*-
import os
import re

import xlsxwriter as xlsxwriter
import time
import xlwt
import xlrd
import xlutils
import shutil
from xlutils.copy import copy
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams

# file_path = u"C:/Users/37646/IdeaProjects/BiTools/pdfs/011001900211_04200064.pdf"
file_path = u"/pdf/readPdf/pdfs"


# file_path = u"C:/Users/37646/IdeaProjects/BiTools/pdf/pdfs/01100190041100070439.pdf"


def inner_key_word():
    key_word = [
        'title','机器编号','发票代码','发票号码','开票日期','校验码','购买方名称','购买方纳税人识别号','购买方地址','电话','密码区','项目名称','车牌号','类型','通行日期起','通行日期止','金额','税率','税额','合计金额','合计税额','价税合计（大写）','价税合计（小写）','销售方名称','销售方纳税人识别号','销售方地址','销售方电话','备注','收款人','复核','开票人'
    ]
    return key_word


class PDFUtils():

    def __init__(self):
        pass

    # 加载路径
    def load_files(self, file_path):
        paths = []
        for path, dir_list, file_list in os.walk(file_path):
            for file_name in file_list:
                abs_path = path+'/'+file_name
                if os.path.isfile(abs_path) and (
                        os.path.splitext(abs_path)[1] == ".pdf" or os.path.splitext(abs_path)[1] == ".PDF"):
                    paths.append(abs_path)
        return paths

    # 循环路径中文件
    def loop_files(self,files):
        contents = []
        for file in files:
            content = self.pdf2txt(file)
            contents.append(content)
        return contents

    # 获取pdf内容
    def pdf2txt(self, file):
        # 打开文件
        with open(file, 'rb') as f:
            # 用文件对象创建一个PDF文档分析器
            praser = PDFParser(f)
            # 创建一个PDF文档，并设置分析器
            doc = PDFDocument(praser)
            # 判断pdf对象是否是可抽取的
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
            # 创建PDF资源管理器，来管理共享资源
            pdfrm = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            # 将资源管理器和设备对象聚合
            device = PDFPageAggregator(pdfrm, laparams=laparams)
            # 创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(pdfrm, device)
            # 循环遍历列表，每次处理一个page内容
            # doc.get_pages()获取page列表

            for page in PDFPage.create_pages(doc):
                contents = ''

                # 使用解析器解析某页数据
                interpreter.process_page(page)
                # 接收该页面的LTPage对象
                layout = device.get_result()
                # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
                # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
                # 想要获取文本就得获取对象的text属性
                for x in layout:
                    if hasattr(x, "get_text"):
                        contents = contents + x.get_text()
                contents = contents + file
            return contents

    # 解析pdf内容
    def checkoutDetail(self, contents):
        # 声明切片接收pdf内容
        results = []
        for content in contents:
            result = {}
            text_line = content.split("\n")
            for index, line in enumerate(text_line):
                item = re.sub(r"\s+", "", line)
                item = item.replace(":", "")
                result["title"] = text_line[3]
                if item == "发票号码":
                    result["发票号码"] = text_line[index + 4]
                    continue
                if item == "发票代码":
                    result["发票代码"] = text_line[index + 4]
                    continue
                if item == "开票日期":
                    result["开票日期"] = text_line[index + 4]
                    continue
                if item == "机器编号":
                    result["机器编号"] = text_line[index + 1]
                    continue
                if item == "校验码":
                    result["校验码"] = text_line[index + 4]
                    continue
                if item == "名称" and text_line[index - 3] == "购":
                    result["购买方名称"] = text_line[index + 5]
                    continue
                if item == "纳税人识别号" and text_line[index - 4] == "购":
                    result["购买方纳税人识别号"] = text_line[index + 5]
                    continue
                if item == "电话" and text_line[index - 6] == "购":
                    result["电话"] = text_line[index + 4].split(" ")[1]
                    continue
                if item == "地址、" and text_line[index - 5] == "购":
                    result["购买方地址"] = text_line[index + 4].split(" ")[0]
                    continue
                if item == "开户行及账号" and text_line[index - 6] == "购":
                    result["购买方开户行及账号"] = text_line[index + 4]
                    continue
                if item == "密":
                    result["密码区"] = text_line[index + 3] + ' ' + text_line[index + 4] + ' ' + text_line[index + 5] + ' ' + \
                                    text_line[index + 6]
                    continue
                if item == "名称" and text_line[index - 3] == "销":
                    result["销售方名称"] = text_line[index + 5]
                    continue
                if item == "纳税人识别号" and text_line[index - 4] == "销":
                    result["销售方纳税人识别号"] = text_line[index + 5]
                    continue
                if item == "电话" and text_line[index - 6] == "销":
                    result["销售方电话"] = text_line[index + 4].split(" ")[1]
                    continue
                if item == "地址、" and text_line[index - 5] == "销":
                    result["销售方地址"] = text_line[index + 5].split(" ")[0]
                    continue
                if item == "开户行及账号" and text_line[index - 6] == "销":
                    result["销售方开户行及账号"] = text_line[index + 4]
                    continue
                if item == "收款人":
                    result["收款人"] = text_line[index + 1]
                    continue
                if item == "复核":
                    result["复核"] = text_line[index + 1]
                    continue
                if item == "开票人":
                    result["开票人"] = text_line[index + 1]
                    continue
                if item == "备":
                    result["备注"] = text_line[index - 1]
                    continue
                if item == "项目名称":
                    result["项目名称"] = text_line[index + 2]
                    continue
                if item == "金额":
                    result["金额"] = text_line[index + 3]
                    continue
                if item == "税率":
                    result["税率"] = text_line[index + 1]
                    continue
                if item == "税额":
                    result["税额"] = text_line[index + 1]
                    continue
                if item == "合":
                    result["合计金额"] = text_line[index + 4]
                    result["合计税额"] = text_line[index + 5]
                    continue
                if item == "车牌号":
                    result["车牌号"] = text_line[index + 2]
                    continue
                if item == "价税合计（大写）":
                    result["价税合计（大写）"] = text_line[index + 1]
                    continue
                if item == "（小写）":
                    result["价税合计（小写）"] = text_line[index + 1]
                    continue
                if item == "类型通行日期起通行日期止":
                    result["类型"] = text_line[index + 1].split(" ")[0]
                    result["通行日期起"] = text_line[index + 1].split(" ")[1]
                    result["通行日期止"] = text_line[index + 2]
                    continue
                if '.pdf' in item:
                    result["file_name"] = text_line[index]
                    continue
            results.append(result)
        return results

    # 数据写入excel
    def write_to_excel(self,key_word,results):
        file_part = str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        # pdf/excel
        workbook = xlsxwriter.Workbook('excel/pdf_data_' + file_part + '.xlsx')
        worksheet = workbook.add_worksheet()

        # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
        # bold：加粗，num_format:数字格式
        bold_format = workbook.add_format({'bold': True})
        #money_format = workbook.add_format({'num_format': '$#,##0'})
        #date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

        # 将二行二列设置宽度为15(从0开始)
        worksheet.set_column(1, 0, 15)

        # 用符号标记位置，例如：A列1行
        worksheet.write('A1', key_word[0], bold_format)
        worksheet.write('B1', key_word[1], bold_format)
        worksheet.write('C1', key_word[2], bold_format)
        worksheet.write('D1', key_word[3], bold_format)
        worksheet.write('E1', key_word[4], bold_format)
        worksheet.write('F1', key_word[5], bold_format)
        worksheet.write('G1', key_word[6], bold_format)
        worksheet.write('H1', key_word[7], bold_format)
        worksheet.write('I1', key_word[8], bold_format)
        worksheet.write('J1', key_word[9], bold_format)
        worksheet.write('K1', key_word[10], bold_format)
        worksheet.write('L1', key_word[11], bold_format)
        worksheet.write('M1', key_word[12], bold_format)
        worksheet.write('N1', key_word[13], bold_format)
        worksheet.write('O1', key_word[14], bold_format)
        worksheet.write('P1', key_word[15], bold_format)
        worksheet.write('Q1', key_word[16], bold_format)
        worksheet.write('R1', key_word[17], bold_format)
        worksheet.write('S1', key_word[18], bold_format)
        worksheet.write('T1', key_word[19], bold_format)
        worksheet.write('U1', key_word[20], bold_format)
        worksheet.write('V1', key_word[21], bold_format)
        worksheet.write('W1', key_word[22], bold_format)
        worksheet.write('X1', key_word[23], bold_format)
        worksheet.write('Y1', key_word[24], bold_format)
        worksheet.write('Z1', key_word[24], bold_format)
        worksheet.write('AA1', key_word[25], bold_format)
        worksheet.write('AB1', key_word[26], bold_format)
        worksheet.write('AC1', key_word[27], bold_format)
        worksheet.write('AD1', key_word[28], bold_format)
        worksheet.write('AE1', key_word[29], bold_format)
        row = 1
        col = 0
        # 使用write_string方法，指定数据格式写入数据
        for item in results:
            try:
                key_word0 = item[key_word[0]]
                key_word1 = item[key_word[1]]
                key_word2 = item[key_word[2]]
                key_word3 = item[key_word[3]]
                key_word4 = item[key_word[4]]
                key_word5 = item[key_word[5]]
                key_word6 = item[key_word[6]]
                key_word7 = item[key_word[7]]
                key_word8 = item[key_word[8]]
                key_word9 = item[key_word[9]]
                key_word10 = item[key_word[10]]
                key_word11 = item[key_word[11]]
                key_word12 = item[key_word[12]]
                key_word13 = item[key_word[13]]
                key_word14 = item[key_word[14]]
                key_word15 = item[key_word[15]]
                key_word16 = item[key_word[16]]
                key_word17 = item[key_word[17]]
                key_word18 = item[key_word[18]]
                key_word19 = item[key_word[19]]
                key_word20 = item[key_word[20]]
                key_word21 = item[key_word[21]]
                key_word22 = item[key_word[22]]
                key_word23 = item[key_word[23]]
                key_word24 = item[key_word[24]]
                key_word25 = item[key_word[25]]
                key_word26 = item[key_word[26]]
                key_word27 = item[key_word[27]]
                key_word28 = item[key_word[28]]
                key_word29 = item[key_word[29]]
                key_word30 = item[key_word[30]]
                # print(key_word0)
                # print(key_word1)
                # print(key_word2)
                # print(key_word3)
                # print(key_word4)
                # print(key_word5)
                # print(key_word6)
                # print(key_word7)
                # print(key_word8)
                # print(key_word9)
                # print(key_word10)
                # print(key_word11)
                # print(key_word12)
                # print(key_word13)
                # print(key_word14)
                # print(key_word15)
                # print(key_word16)
                # print(key_word17)
                # print(key_word18)
                # print(key_word19)
                # print(key_word20)
                # print(key_word21)
                # print(key_word22)
                # print(key_word23)
                # print(key_word24)
                # print(key_word25)
                # print(key_word26)
                # print(key_word27)
                # print(key_word28)
                # print(key_word29)
                # print(key_word30)
                # print('-------------------')
            except Exception:
                file_path = item['file_name']
                file_name = './pdf_todo/' + file_path.split('/')[-1]
                shutil.move(file_path,file_name)
            row = row + 1
            continue
        workbook.close()


if __name__ == '__main__':
    path = file_path
    pdf_utils = PDFUtils()
    files = pdf_utils.load_files(path)
    print(files)
    contents = pdf_utils.loop_files(files)
    results = pdf_utils.checkoutDetail(contents)
    key_word = inner_key_word()
    pdf_utils.write_to_excel(key_word,results)