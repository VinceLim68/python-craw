#-*- coding:utf-8 -*-
from Tkinter import *

master = Tk()

#觉得这种获得listbox值的方法好笨
def do():
    #print theLB.get(ANCHOR)        #单选时可以用ANCHOR关键字
    #以下是得到多选列表的所有值的文本内容
    sel = theLB.curselection()        #得到选中的index
    for i in sel:
        print theLB.get(i)

theLB = Listbox(master,selectmode = EXTENDED)
theLB.pack()

for item in ['a','b','c','d']:
    theLB.insert(END,item)

#我只能用button的方法来获得listbox的值
b = Button(master,text = 'see', command = do)
b.pack()

mainloop()