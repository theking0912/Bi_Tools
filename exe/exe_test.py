# -*- coding: utf-8 -*-
from tkinter import *
from PIL import Image, ImageTk


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master,bg='black')
        self.pack(expand=YES,fill=BOTH)
        self.window_init()
        self.createWidgets()

    def window_init(self):
        self.master.title('welcome to video-captioning system')
        width,height=self.master.maxsize()
        self.master.geometry("{}x{}".format(width, height))

    def createWidgets(self):
        # fm1
        self.fm1=Frame(self,bg='black')
        self.titleLabel=Label(self.fm1,text="video-captioning system",font=('微软雅黑',64),fg = "white",bg='black')
        self.titleLabel.pack()
        self.fm1.pack(side= TOP,expand=YES,fill='x',pady=20)

        # fm2
        self.fm2=Frame(self,bg='black')
        self.fm2_left=Frame(self.fm2,bg='black')
        self.fm2_right=Frame(self.fm2,bg='black')
        self.fm2_left_top=Frame(self.fm2_left,bg='black')
        self.fm2_left_bottom=Frame(self.fm2_left,bg='black')

        self.predictEntry=Entry(self.fm2_left_top,font=('微软雅黑',24),width='72',fg='#FF4081')
        self.predictButton=Button(self.fm2_left_top,text='predict sentence',bg='#FF4081',fg='white',font=('微软雅黑',36),width='16',command=self.output_predict_sentence)
        self.predictButton.pack(side=LEFT)
        self.predictEntry.pack(side=LEFT,fill='y',padx=20)
        self.fm2_left_top.pack(side=TOP,fill='x')

        self.truthEntry=Entry(self.fm2_left_bottom,font=('微软雅黑',24),width='72',fg='#22C9C9')
        self.truthButton=Button(self.fm2_left_bottom,text='ground truth',bg='#22C9C9',fg='white',font=('微软雅黑',36),width='16',command=self.output_ground_truth)
        self.truthButton.pack(side=LEFT)
        self.truthEntry.pack(side=LEFT,fill='y',padx=20)
        self.fm2_left_bottom.pack(side=TOP,pady=10,fill='x')

        self.fm2_left.pack(side=LEFT,padx=60,pady=20,expand=YES,fill='x')
        # self.nextVideoImg= ImageTk.PhotoImage(file = '/home/hl/Desktop/lovelyqian/nextVideo.png')

        # self.nextVideoButton=Button(self.fm2_right,image=self.nextVideoImg,text='next video',bg='black',command=self.start_play_video_thread)
        # self.nextVideoButton.pack(expand=YES,fill=BOTH)
        self.fm2_right.pack(side=RIGHT,padx=60)
        self.fm2.pack(side=TOP,expand=YES,fill="x")

        # fm3
        self.fm3=Frame(self,bg='black')
        load = Image.open('C:/Users/37646/IdeaProjects/BiTools/pdf/images/20191202160224.jpg')
        initIamge= ImageTk.PhotoImage(load)
        self.panel = Label(self.fm3,image=initIamge)
        self.panel.image = initIamge
        self.panel.pack()
        self.fm3.pack(side=TOP,expand=YES,fill=BOTH,pady=10)

    def output_predict_sentence(self):
        predicted_sentence_str='hello world.'
        self.predictEntry.delete(0,END)
        self.predictEntry.insert(0,predicted_sentence_str)

    def output_ground_truth(self):
        ground_truth='this is ground truth.'
        self.truthEntry.delete(0,END)
        self.truthEntry.insert(0,ground_truth)

if __name__=='__main__':
    app = Application()
    # to do
    app.mainloop()