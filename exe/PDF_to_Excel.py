# -*- coding: utf-8 -*-
import re
import os
import sys
import time
import codecs
import shutil
import threading
import xlsxwriter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, qApp, \
    QDesktopWidget, QFileDialog, QPlainTextEdit

# file_path = u"C:/Users/37646/IdeaProjects/BiTools/pdf/pdfs/"

def inner_key_word():
    key_word = [
        'title','机器编号','发票代码','发票号码','开票日期','校验码','购买方名称','购买方纳税人识别号','购买方地址','电话','密码区','项目名称','车牌号','类型','通行日期起','通行日期止','金额','税率','税额','合计金额','合计税额','价税合计（大写）','价税合计（小写）','销售方名称','销售方纳税人识别号','销售方地址','销售方电话','备注','收款人','复核','开票人'
    ]
    return key_word


class PDFUtils():

    def __init__(self):
        pass
    # 加载路径
    def load_folders(self,path):
        folders = os.listdir(path)
        paths = []
        curr_path = []
        for folder in folders:
            if os.path.isdir(os.path.join(path, folder)):
                abs_path = os.path.join(path, folder)
                paths.append(abs_path)
                curr_path.append(folder)
        return paths, curr_path

    # 加载文件
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

    # 数据写入txt
    def write_to_txt(self,excel_dir,contents):
        file_part = str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        full_path = excel_dir + '/pdf_full_text_' + file_part + '.txt'  # 也可以创建一个.doc的word文档
        file = codecs.open(full_path, 'w','utf-8')
        for i in range(len(contents)):
            file.write(str(contents[i]))
        file.close()

    # 数据写入excel
    def write_to_excel(self,pdf_todo_dir,excel_dir,key_word,results):
        file_part = str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        # pdf/excel
        workbook = xlsxwriter.Workbook(excel_dir + '/pdf_data_' + file_part + '.xlsx')
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
                worksheet.write_string(row, col, item[key_word[0]])
                worksheet.write_string(row, col + 1, item[key_word[1]])
                worksheet.write_string(row, col + 2, item[key_word[2]])
                worksheet.write_string(row, col + 3, item[key_word[3]])
                worksheet.write_string(row, col + 4, item[key_word[4]])
                worksheet.write_string(row, col + 5, item[key_word[5]])
                worksheet.write_string(row, col + 6, item[key_word[6]])
                worksheet.write_string(row, col + 7, item[key_word[7]])
                worksheet.write_string(row, col + 8, item[key_word[8]])
                worksheet.write_string(row, col + 9, item[key_word[9]])
                worksheet.write_string(row, col + 10, item[key_word[10]])
                worksheet.write_string(row, col + 11, item[key_word[11]])
                worksheet.write_string(row, col + 12, item[key_word[12]])
                worksheet.write_string(row, col + 13, item[key_word[13]])
                worksheet.write_string(row, col + 14, item[key_word[14]])
                worksheet.write_string(row, col + 15, item[key_word[15]])
                worksheet.write_string(row, col + 16, item[key_word[16]])
                worksheet.write_string(row, col + 17, item[key_word[17]])
                worksheet.write_string(row, col + 18, item[key_word[18]])
                worksheet.write_string(row, col + 19, item[key_word[19]])
                worksheet.write_string(row, col + 20, item[key_word[20]])
                worksheet.write_string(row, col + 21, item[key_word[21]])
                worksheet.write_string(row, col + 22, item[key_word[22]])
                worksheet.write_string(row, col + 23, item[key_word[23]])
                worksheet.write_string(row, col + 24, item[key_word[24]])
                worksheet.write_string(row, col + 25, item[key_word[25]])
                worksheet.write_string(row, col + 26, item[key_word[26]])
                worksheet.write_string(row, col + 27, item[key_word[27]])
                worksheet.write_string(row, col + 28, item[key_word[28]])
                worksheet.write_string(row, col + 29, item[key_word[29]])
                worksheet.write_string(row, col + 30, item[key_word[30]])
            except Exception:
                file_path = item['file_name']
                file_name = pdf_todo_dir + '/' + file_path.split('/')[-1]
                shutil.move(file_path,file_name)
            row = row + 1
        workbook.close()

class MYGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.exit_flag = False
        self.try_time = 1527652647.6671877 + 24 * 60 * 60

        self.initUI()

    def initUI(self):
        self.pdf_label = QLabel("PDF文件夹路径: ")
        self.pdf_btn = QPushButton("选择")
        self.pdf_btn.clicked.connect(self.open_pdf)
        self.pdf_path = QLineEdit("PDF文件夹路径...")
        self.pdf_path.setEnabled(False)
        self.info = QPlainTextEdit()

        h1 = QHBoxLayout()
        h1.addWidget(self.pdf_label)
        h1.addWidget(self.pdf_path)
        h1.addWidget(self.pdf_btn)

        self.run_btn = QPushButton("运行")
        self.run_btn.clicked.connect(self.run)

        # self.auth_label = QLabel("密码")
        # self.auth_ed = QLineEdit("secrity key")

        exit_btn = QPushButton("退出")
        exit_btn.clicked.connect(self.Exit)
        h4 = QHBoxLayout()
        # h4.addWidget(self.auth_label)
        # h4.addWidget(self.auth_ed)
        h4.addStretch(1)
        h4.addWidget(self.run_btn)
        h4.addWidget(exit_btn)

        # v = QVBoxLayout()
        # v.addLayout(h1)
        # v.addWidget(self.info)
        # self.setLayout(v)
        # width = int(QDesktopWidget().screenGeometry().width() / 3)
        # height = int(QDesktopWidget().screenGeometry().height() / 3)
        # self.setGeometry(100, 100, width, height)
        # self.setWindowTitle('PDF to Excel')
        # self.show()

        v = QVBoxLayout()
        v.addLayout(h1)
        v.addWidget(self.info)
        v.addLayout(h4)
        self.setLayout(v)
        width = int(QDesktopWidget().screenGeometry().width() / 3)
        height = int(QDesktopWidget().screenGeometry().height() / 3)
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle('PDF to Excel')
        self.show()

    def open_pdf(self):
        fname = QFileDialog.getExistingDirectory(self, "Open pdf folder",
                                                 "/home")
        if fname:
            self.pdf_path.setText(fname)

    def run(self):
        self.info.setPlainText("")
        threading.Thread(target=self.scb, args=()).start()
        self.info.insertPlainText("密码正确，开始运行程序!\n")
        threading.Thread(target=self.main_fcn, args=()).start()

    def Exit(self):
        self.exit_flag = True
        qApp.quit()

    def scb(self):
        flag = True
        cnt = self.info.document().lineCount()
        while not self.exit_flag:
            if flag:
                self.info.verticalScrollBar().setSliderPosition(self.info.verticalScrollBar().maximum())
            time.sleep(0.01)
            if cnt < self.info.document().lineCount():
                flag = True
                cnt = self.info.document().lineCount()
            else:
                flag = False
            time.sleep(0.01)

    def main_fcn(self):
        pdf_utils = PDFUtils()
        # 创建excel输出文件夹
        pdf_dir = self.pdf_path.text()
        self.info.insertPlainText("excel目录生成成功！\n")
        excel_dir = pdf_dir.replace('pdfs','excel')
        if not os.path.isdir(excel_dir):
            os.mkdir(excel_dir)

        # 创建pdf_todo收录文件夹
        self.info.insertPlainText("pdf_todo目录生成成功！\n\n")
        pdf_todo_dir = pdf_dir.replace('pdfs','pdf_todo')
        if not os.path.isdir(pdf_todo_dir):
            os.mkdir(pdf_todo_dir)

        # 加载文件夹
        if os.path.isdir(self.pdf_path.text()):
            try:
                files = pdf_utils.load_files(self.pdf_path.text())
            except Exception:
                self.info.insertPlainText("加载PDF文件夹出错，请重试！\n\n")
                return
        else:
            return

        # 获取所有文件内容
        contents = pdf_utils.loop_files(files)

        # 写全部数据到txt
        pdf_utils.write_to_txt(excel_dir,contents)

        # 格式化pdf文件
        results = pdf_utils.checkoutDetail(contents)
        key_word = inner_key_word()

        # 数据存储到excel
        pdf_utils.write_to_excel(pdf_todo_dir,excel_dir,key_word,results)

        self.info.insertPlainText("解析结束！\n")
        self.info.insertPlainText("发票内容excel输出路径在：\n"+excel_dir+"\n")
        self.info.insertPlainText("异常pdf文件收录在：\n"+pdf_todo_dir+"\n")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MYGUI()
    sys.exit(app.exec_())
    ex.main_fcn()