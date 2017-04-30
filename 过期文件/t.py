#-*- coding:utf-8 -*-
from Tkinter import *

master = Tk()

#觉得这种获得listbox值的方法好笨
# def do(event):
def do():
    # print theLB.get(ANCHOR)
    # print theLB.curselection()
    # print theLB.get(1)
    for i in theLB.curselection():
        print theLB.get(i)
    # print var

# var = StringVar()
# theLB = Listbox(master,selectmode = EXTENDED,  listvariable = var)
theLB = Listbox(master,selectmode = EXTENDED)
theLB.pack()

# theLB.bind('<ButtonRelease-1>', do)

for item in ['a','b','c','d']:
    theLB.insert(END,item)

#我只能用button的方法来获得listbox的值
b = Button(master,text = 'see', command = do)
b.pack()

# v.set(theLB.curselection())
# l = Label(master, textvariable=v)
# l.pack()

mainloop()