#coding:utf-8
# 通过数据库查询记录，并可记录到询价数据库中
import MySQLdb
import sys
import xlsxwriter
import datetime
import time
from Tkinter import *
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding("utf-8")

class DataStat(object):

	def __init__(self):
		self.datas = []				#存放传入的数据
		self.xjr = { 
			"hyx":"黄燕翔","jq":"贾琴","jz":"金忠","lyx":"廖亚香","czy":"陈志艳","xz":"项争","cyw":"陈玉炜","gs":"公司外部","kc":"柯琛",
			"lmc":"林美彩","clh":"陈丽华","wml":"吴木兰","cym":"陈幼梅","cjy":"陈军勇","zly":"朱黎英","wj":"吴洁","wlt":"伍灵婷"
			}

	def stat(self,li):
		s_result = {}
		#求列表里的基本统计数据
		if len(li) < 1:
			print("没有可供统计分析的数据")
			return
		li.sort()
		s_result['num'] = len(li)
		s_result['max'] = max(li)
		s_result['min'] = min(li)
		s_result['sum_of_item'] = float(sum(i for i in li))
		sum_of_squares = sum(i**2 for i in li)
		s_result['avg'] = s_result['sum_of_item'] /  s_result['num']
		s_result['stdev'] = ((s_result['num'] * sum_of_squares - s_result['sum_of_item'] ** 2) / (s_result['num']**2))**0.5
		s_result['中位数'] = (li[s_result['num']/2] + li[s_result['num']/2 -1])/2.0 if s_result['num']%2 == 0 else li[s_result['num']/2]
		s_result['20'] = li[s_result['num']/5]
		s_result['40'] = li[s_result['num']/5*2]
		s_result['60'] = li[s_result['num']/5*3]
		s_result['80'] = li[s_result['num']/5*4]		
		return s_result


	def get_anlyse(self,community,li):
		if len(li) < 1:
			print("没有可供统计分析的数据")
			return

		#先把最高和最低的两个记录去掉，避免录入错误严重影响偏差。
		li.sort()
		num_list = len(li)
		print "Now have %s datas"%num_list
		if num_list < 20:
			self.pri("这是个不活跃小区，数据少于20个,所以没有做去除工作")
		else:
			num_del = int(num_list / 200)
			if num_del < 2:	num_del = 2
			for i in range(0,num_del):
				del li[0]
				del li[-i]
		print "After clear there is %s datas"%len(li)
		
		result = self.stat(li)

		#把times个标准差之外的数据清除，生成一个新列表,理论上能覆盖近90%的数据
		times = 1.5 		#标准差的倍数
		times_stdev_top = times * result['stdev'] + result['avg']
		times_stdev_bottom = result['avg'] - times * result['stdev'] 
		new_li = []
		for i in li:
			if i <= times_stdev_top and i >= times_stdev_bottom:
				new_li.append(i)
		
		new_result = self.stat(new_li)

		return result,new_result

	def pri(self,comm,newresult):
		# result,new_result = self.get_anlyse(comm,price)
		info = ''
		info = info + "*************  覆盖" + comm + "90% 数据分布情况 ************\n"
		info = info + self.pri_info(newresult)

		return info


		
	def pri_info(self,res):
		#输出数列的评估结果
		info = ''
		info = info + "本次共有 %u个数据\n" %(res['num'])
		info = info + "标准差为：%9.2f，标准差系统为：%5.2f %%\n"%(res['stdev'],res['stdev']/res['avg']*100)
		info = info + "        0     **    20%    **    40%    **    60%    **    80%    **    100%    \n"
		info = info + "    %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f \n"%(res['min'],res['20'],res['40'],res['60'],res['80'],res['max'])
		info = info + "中位数：%9.2f ,平均价: %9.2f\n"%(res['中位数'],res['avg'])
		info = info + "评估价为 %9.2f ,价格区间 %9.2f - %9.2f\n"%(res['中位数']*0.82,res['中位数']*0.8,res['中位数']*0.90)
		info = info + "总审价：%9.2f\n"%(res['60'])
		return info


	def out_xlsx(self,keywords,datas):
		fout = xlsxwriter.Workbook(keywords.decode() + 'SQL.xlsx')
		worksheet = fout.add_worksheet('')
		amount = 0  #记录总数
		row = 1     #记录行
		title = ['序号','项目','面积','户型','单价','层次','总楼层','建成年份','朝向','总价','网址','小区']
		worksheet.write_row('A1',title)
		for data in datas:
		    amount = amount + 1
		    worksheet.write(row,0,amount)
		    worksheet.write(row,1,data[3])
		    worksheet.write(row,2,data[1])
		    worksheet.write(row,3,data[4])
		    worksheet.write(row,4,data[0])
		    worksheet.write(row,5,data[2])
		    worksheet.write(row,6,data[5])
		    worksheet.write(row,7,data[6])
		    worksheet.write(row,8,data[7])
		    worksheet.write(row,9,data[8])
		    worksheet.write(row,10,data[9])
		    worksheet.write(row,11,data[10])
		    row = row + 1
		fout.close()

	def Imprint(self):
		print "YEs I do"

	def out_enquiry(self,v2,comm_name,xj):
		if v2['stdev']/v2['avg']*100 >10:
			print "标准差系统过大，数据有效性不足"
			return
		
		now = datetime.date.today()
		who = self.xjr[xj]
		total_f = []
		build_y = []

		for data in datas:
			total_f.append(filter(str.isdigit,str(data[5])))
			if int(filter(str.isdigit,str(data[6]))) > 1800:
				build_y.append(filter(str.isdigit,str(data[6])))

		avg_t_floor = (sum(int(i) for i in total_f))/len(total_f)
		avg_b_year = (sum(int(i) for i in build_y))/len(build_y)
		
		year = str(avg_b_year) + "-01-01 00:00:00"
		
		price = int(v2['中位数']*0.82)
		memo = "%s个数据，挂牌区间%.0f-%.0f"%(v2['num'],v2['min'],v2['80'])
		elevator = "带电梯" if avg_t_floor > 8 else "无电梯"
		struct = "钢混结构" if avg_t_floor > 7 else "砖混结构"
		memo1 = "二手房评估可以%.0f"%(round(float(v2['20'])/100,0)*100)

		print datetime.date.today(),comm_name,memo1,avg_floor,avg_t_floor,who,price,memo,year,struct,elevator
		

		db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "apprsal_cdh",charset = "utf8")
		cursor = db.cursor()
		try:
			sql_equiry ="INSERT t_enquiry (Enquiry_Date,Enquiry_CellName,PA_Located,PA_Level,Apprsal_Use,Enquiry_PmName,\
				OfferPeople,Apprsal_Up,Enquiry_Source,Remark,Enquiry_Layout,PA_YearBuilt,PA_Structure,PA_Elevator)\
			                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql_equiry,(datetime.date.today(),comm_name,memo1,avg_floor,"住宅",who,"林晓",price,"估价师报价",memo,avg_t_floor,year,struct,elevator))
			db.commit()
		except:
			print "~~~ Wo，fault!!!~~~~~~"
		finally:
			cursor.close()
			db.close()

if __name__=="__main__":

	def sstat():
		global price,area,floor,unit_price,T_floor
		price = []
		area = []
		floor = []
		unit_price = []
		T_floor = []


		comm = e.get().encode()
		db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
		cursor = db.cursor()
		# comm = "珍珠湾花园"
		
		xjr = ""
		sql = "SELECT price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
		details_url,community_name FROM for_sale_property WHERE community_name LIKE '%%%s%%'"%comm
		sql_comms = "SELECT community_name FROM for_sale_property WHERE community_name LIKE '%%%s%%' group by community_name"%comm

		cursor.execute(sql)
		datas = cursor.fetchall()
		cursor.execute(sql_comms)
		cs = cursor.fetchall()
		cursor.close()
		db.close()
		data_stat = DataStat()
		info = ''

		for c in cs:
			info = info + c[0] + '\n'

		if len(datas) == 0 :
			info = info + "There is no datas in this community,check you community name and try again ......\n"
		else:
			for data in datas:
				if data[2] > 0 : floor.append(data[2])			#4.16修改
				unit_price.append(data[0])
				area.append(data[1])
				price.append(data[0])
				T_floor.append(data[5])
			try:
				data_stat.out_xlsx(comm,datas)
			except:
				info = info + "Save the EXCEL file failed\n"
			result,new_result = data_stat.get_anlyse(comm,unit_price)
			info = info + data_stat.pri(comm,new_result)
			avg_area = int(sum(i for i in area))/len(area)
			avg_floor = int(sum(int(i) for i in floor)/len(floor))
			info = info + "平均面积为 %6.0f\n"%(avg_area)
			info = info + "平均楼层为 %6.0f\n"%(avg_floor)
			
			if xjr:
				data_stat.out_enquiry(v2,comm,xjr)

			resTxt.config(text = info)

	def draw1():
		# print '+'*50
		global price,area
		plt.plot(area,price,'o')
		plt.show()
	
	def draw2():

		global price,T_floor
		plt.plot(T_floor,price,'o')
		plt.show()


				
	
	master = Tk()
	
	price = []
	area = []
	floor = []
	unit_price = []
	T_floor = []

	data_stat = DataStat()

	master.geometry('600x600+130+140')
	master.title('房价自动询价系统4.0 by 林晓')

	toolbar1 = Frame(master,height = 25, bg = 'light sea green')

	w = Label(toolbar1, text="请输入拟查询的小区名:",bg = 'light sea green',padx = 5, font=("华文仿宋", 14))
	w.pack(side = LEFT,padx = 35)

	e = Entry(toolbar1,font=("Helvetica", 12))
	e.pack(side = LEFT)
	e.focus_set()
	toolbar1.pack(fill = X )

	toolbar2 = Frame(master,height = 25, bg = 'light sea green')

	toolbar2.pack(fill = X )

	quote_Button = Button(toolbar2, text = '请报价',command = data_stat.Imprint)
	quote_Button.pack(padx = 35,pady = 5,side = LEFT)
	stat_Button = Button(toolbar2, text = '面积-单价',command = draw1)
	stat_Button.pack(padx = 35,pady = 5,side = LEFT)
	stat_Button = Button(toolbar2, text = '总楼层-单价',command = draw2)
	stat_Button.pack(padx = 35,pady = 5,side = LEFT)



	status = Label(master,text = '林晓',bd = 1,relief = SUNKEN,anchor =CENTER)
	status.pack(side = BOTTOM ,fill = X)

	resTxt = Label(master, text="", font=("华文仿宋", 12),bg = 'antique white')
	resTxt.pack(expand = YES,fill = BOTH)


	mainloop()







