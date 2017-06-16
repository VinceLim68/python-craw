#-*- coding:utf-8 -*-
from Tkinter import *
import data_stat
import os
import matplotlib.pyplot as plt
from spider import mytools

class HouseQuote(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master,bg = 'CadetBlue2')
        self.grid()
        self.create_win()
        self.data_stat = data_stat.DataStat()
        self.master.title('房价自动询价系统4.0 by 林晓')
        self.v = {}

    def quotation(self):
        # 这是主询价
        self.comm = self.e_comm.get().encode().strip()
        if self.comm == '':
            self.resTxt.config(text = '没有待查询小区')
            return
        self.info,self.v = self.data_stat.query_main(self.comm)
        self.print_info()


    def print_info(self):
        # 输出分析结果

        if isinstance(self.v, str):                                 #2016.6.16如果没有查询到数据会出错，这里增加一个判断
            brief = '未查询到相关数据'
        else:
            brief = '%s(%.0f) \n******************\n 抵押评估价：%9.2f \n\n（按揭评估价：%9.2f)\n\n标准差系数：%9.2f'%(self.v['comm'].strip(),
                self.v['final_len'],self.v['final_中位数']*0.82,self.v['final_20'],self.v['final_stdev']/self.v['final_avg']*100)

        self.resTxt.config(text = brief)

        # 以下是往列表里插入小区名称、面积、楼层，形成各自的列表
        self.l_comm.delete(0, END)
        if self.v != '':
            for item in self.data_stat.d:
                self.l_comm.insert(END,item)

            area = list(set(zip(*self.data_stat.datas)[1]))
            area.sort()
            self.l_area.delete(0, END)
            for item in area:
                self.l_area.insert(END,item)

            floors = list(set(zip(*self.data_stat.datas)[5]))
            floors.sort()
            self.l_floors.delete(0, END)
            for item in floors:
                self.l_floors.insert(END,item)
        # self.d = collections.Counter(zip(*self.datas)[10]) 
        # for item in collections.Counter(zip(*self.data_stat.datas)[1]):


    def show_comm_and_nums(self):
        top = Toplevel()
        msg = ''
        for k in self.data_stat.d:
            msg = msg + "%s : %s\n"%(k,self.data_stat.d[k])
            # k是lst中的每个元素
            # d[k]是k在lst中出现的次数
        Message(top,text = msg,font=("微软雅黑", 12)).pack()

    @mytools.exeTime
    def show_area_price(self):
        if len(self.v) == 0:
            self.resTxt.config(text = '没有可展示数据')
            return

        max_area = max(zip(*self.data_stat.final_data)[1]) * 1.2
        min_area = min(zip(*self.data_stat.final_data)[1]) * 0.8
        max_price = self.v['final_max'] * 1.2
        min_price = self.v['final_min'] * 0.8
        plt.axis([min_area,max_area,min_price,max_price])
        plt.axhline( y = self.v['final_20'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_中位数'],linestyle = 'dotted',color = "red")
        plt.axhline( y = self.v['final_40'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_60'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_80'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_min'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_max'],linestyle = 'dotted')
        # plt.axhline( x =40)
        plt.title("The area-price")
        plt.xlabel("Area")
        plt.ylabel("Price")

        plt.plot(zip(*self.data_stat.final_data)[1],zip(*self.data_stat.final_data)[0],'o')
        plt.show()
    
    def show_floor_price(self):
        if len(self.v) == 0:
            self.resTxt.config(text = '没有可展示数据')
            return
        max_floor = max(zip(*self.data_stat.final_data)[5]) *1.2
        min_floor = min(zip(*self.data_stat.final_data)[5]) *0.8
        max_price = self.v['final_max'] * 1.2
        min_price = self.v['final_min'] * 0.8
        plt.axis([min_floor,max_floor,min_price,max_price])
        plt.axhline( y = self.v['final_20'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_40'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_60'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_80'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_min'],linestyle = 'dotted')
        plt.axhline( y = self.v['final_max'],linestyle = 'dotted')
        # plt.axhline( x =40)
        plt.title("The floor-price")
        plt.xlabel("Total floor")
        plt.ylabel("Price")
        # plt.axis([0,max_floor,min_price,max_price])
        plt.plot(zip(*self.data_stat.final_data)[5],zip(*self.data_stat.final_data)[0],'o')
        plt.show()
    
    def show_details(self):
        topdetail = Toplevel()
        self.info = self.data_stat.info
        Message(topdetail,text = self.info, font=("微软雅黑", 12)).pack()

    def excel(self):
        # 生成excel表格并打开
        self.comm = self.e_comm.get().encode().strip()
        if self.comm == '':
            self.resTxt.config(text = '没有待查询小区')
        else:
            fname = self.data_stat.out_xlsx(self.comm)
            os.startfile(fname)

    def out_query(self):
        self.data_stat.out_enquiry(self.v,'gs')

    def show_comms(self):
        for i in self.l_comm.curselection():
            print i
            print self.l_comm.get(i)

    def put_areas(self):
        sel = self.l_area.curselection()        #得到选中的index
        area_text = ""
        area_list = []
        for i in sel:
            area_list.append(int(self.l_area.get(i)))
            # 列表中取出的area是字符型
            # print(type(self.l_area.get(i)))
            # print(area_list)
            # 数据库里取出的area字段是long
        
        self.e_area.delete(0, END)
        self.e_area.insert(0, area_list)
        record_by_area = self.data_stat.query_again_by_area_or_totalfloor(area_list)
        self.v = self.data_stat.get_anlyse(self.comm,record_by_area)
        self.print_info()
        # print len(record_by_area)
        # for item in record_by_area:
        #     for i in item :
        #         print i
        #     print("*"*50)

        # print area_text
        # self.e_area.config(text = area_text)

    
    def create_win(self):
        
        Label(self, text="待查询小区:", font=("微软雅黑", 12),bg = 'DarkSeaGreen2').grid(row = 0, stick = E, padx = 5, pady = 5)
        self.e_comm = Entry(self)
        self.e_comm.grid(row = 0 ,column = 1, columnspan = 3, stick = N+S+W+E, padx = 5, pady = 5)
        self.b_quotation = Button(self, text = '开始报价', font=("微软雅黑", 14), bg = 'IndianRed1', command = self.quotation
            ).grid(row = 0 ,column = 4,rowspan =3, stick = N+S+W+E, padx = 5, pady = 5)


        Label(self, text="面积:", font=("微软雅黑", 12),bg = 'DarkSeaGreen2').grid(row = 1, stick = E, padx = 5, pady = 5)
        self.e_area = Entry(self,width = 18)
        self.e_area.grid(row = 1 ,column = 1, columnspan = 3, stick = N+S+W+E, padx = 5, pady = 5)
        Label(self, text="总楼层:", font=("微软雅黑", 12),bg = 'DarkSeaGreen2').grid(row = 2,column = 0, stick = E, padx = 5, pady = 5)
        self.e_floors = Entry(self,width = 18)
        self.e_floors.grid(row = 2 ,column = 1, columnspan = 3, stick = N+S+W+E, padx = 5, pady = 5)

        Button(self, text = '小区名称', bg = 'LightYellow3',width = 18 ,command = self.show_comm_and_nums).grid(row = 3 , stick = N+S+W+E, padx = 5, pady = 5)
        b_change_comm_name = Button(self, text = '把小区名称改为', bg = 'LightYellow3',command = self.show_comms).grid(row = 3 ,column = 1, stick = N+S+W+E, padx = 5, pady = 5)
        self.e_new_comm_name = Entry(self,width = 18)
        self.e_new_comm_name.grid(row = 3 ,column = 2, columnspan = 2, stick = N+S+W+E, padx = 5, pady = 5)
        b_area_choice = Button(self, text = '面积选择', bg = 'LightYellow3',command = self.put_areas).grid(row = 3 ,column = 4, stick = N+S+W+E, padx = 5, pady = 5)

        self.l_comm = Listbox(self,selectmode = EXTENDED,exportselection = TRUE)
        self.l_comm.grid(row = 4,column = 0, rowspan = 13 ,stick = N + S, padx = 5, pady = 5)
        self.l_area = Listbox(self,selectmode = EXTENDED)
        self.l_area.grid(row = 4,column = 4, rowspan = 6 , stick = N+S+W+E, padx = 5, pady = 5)

        b_floors_choice = Button(self, text = '总楼层选择', bg = 'LightYellow3').grid(row = 10 ,column = 4, stick = N+S+W+E, padx = 5, pady = 5)
        self.l_floors = Listbox(self,selectmode = EXTENDED)
        self.l_floors.grid(row = 11,column = 4, rowspan = 6 , stick = N+S+W+E, padx = 5, pady = 5)

        self.resTxt = Label(self, text="", font=("微软雅黑", 18))
        self.resTxt.grid(row = 4, column = 1 ,rowspan = 13, columnspan = 3,stick = N+S+W+E, padx = 5, pady = 5)

        b_area_price = Button(self, text = '面积/单价', bg = 'LightYellow3',width = 18,command = self.show_area_price).grid(row = 17 ,column = 0, stick = N+S+W+E, padx = 5, pady = 5)
        b_floors_price = Button(self, text = '总楼层/单价', bg = 'LightYellow3',width = 18,command = self.show_floor_price).grid(row = 17 ,column = 1, stick = N+S+W+E, padx = 5, pady = 5)
        b_out_excel = Button(self, text = '生成EXCEL表格', bg = 'LightYellow3',width = 18, command = self.excel).grid(row = 17 ,column = 2, stick = N+S+W+E, padx = 5, pady = 5)
        b_detail_info = Button(self, text = '详细信息', bg = 'LightYellow3',width = 18,command = self.show_details).grid(row = 17 ,column = 3, stick = N+S+W+E, padx = 5, pady = 5)
        b_out_query = Button(self, text = '生成询价记录', bg = 'LightYellow3',width = 18, command = self.out_query).grid(row = 17 ,column = 4, stick = N+S+W+E, padx = 5, pady = 5)

        # mainloop()

if __name__=="__main__":
    mywin = HouseQuote()
    mywin.mainloop()