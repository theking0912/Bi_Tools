#_*_coding:utf-8_*_
from pdf2image import convert_from_path

file_path = u"C:/Users/37646/IdeaProjects/BiTools/pdf_file/011001900211_04200064.pdf"
# file_path = u"C:/Users/37646/IdeaProjects/BiTools/pdf_file/01100190041100070439.pdf"

if __name__ == '__main__':
    convert_from_path('a.pdf', 500, "output",fmt="JPEG",output_file="ok",thread_count=4)