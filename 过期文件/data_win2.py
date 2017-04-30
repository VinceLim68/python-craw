#coding:utf-8
# 通过数据库查询记录，并可记录到询价数据库中
from __future__ import print_function
import MySQLdb
import sys
import xlsxwriter
import datetime
import time
import collections
reload(sys)
sys.setdefaultencoding("utf-8")
import matplotlib.pyplot as plt

def exeTime(func):  
    def newFunc(*args, **args2):  
        t0 = time.time()  
        # print ("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))  
        back = func(*args, **args2)  
        # print ("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)  )
        print( "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)  )
        return back  
    return newFunc 

class DataStat(object):

	def __init__(self):
		self.clear_datas = []				#存放传入的数据
		self.xjr = { 
			"hyx":"黄燕翔","jq":"贾琴","jz":"金忠","lyx":"廖亚香","czy":"陈志艳","xz":"项争","cyw":"陈玉炜","gs":"公司外部","kc":"柯琛",
			"lmc":"林美彩","clh":"陈丽华","wml":"吴木兰","cym":"陈幼梅","cjy":"陈军勇","zly":"朱黎英","wj":"吴洁","wlt":"伍灵婷"
			}


	# def stat(self,li,keyindex):
	# 	#传入查询的出来的记录：多维列表,keyindex表示分析的是第几个元素（从0开始）
	# 	s_result = {}
	# 	#求列表里的基本统计数据
	# 	if len(li) < 1:
	# 		pri_info("没有可供统计分析的数据")
	# 		return

	# 	s_result['num'] = len(li)
	# 	s_result['max'] =li[-1][keyindex]
	# 	s_result['min'] = li[0][keyindex]
	# 	s_result['sum_of_item'] = float(sum(i[keyindex] for i in li))
	# 	sum_of_squares = sum(i[keyindex]**2 for i in li)
	# 	s_result['avg'] = s_result['sum_of_item'] /  s_result['num']
	# 	s_result['stdev'] = ((s_result['num'] * sum_of_squares - s_result['sum_of_item'] ** 2) / (s_result['num']**2))**0.5

	# 	s_result['中位数'] = (li[s_result['num']/2][keyindex] + li[s_result['num']/2 -1][keyindex])/2.0 if s_result['num']%2 == 0 else li[s_result['num']/2][keyindex]
	# 	s_result['20'] = li[s_result['num']/5][keyindex]
	# 	s_result['40'] = li[s_result['num']/5*2][keyindex]
	# 	s_result['60'] = li[s_result['num']/5*3][keyindex]
	# 	s_result['80'] = li[s_result['num']/5*4][keyindex]	
	
	# 	return s_result

	def stat(self,li):
		#传入查询的出来的记录：多维列表,keyindex表示分析的是第几个元素（从0开始）
		s_result = {}
		#求列表里的基本统计数据
		if len(li) < 1:
			pri_info("没有可供统计分析的数据")
			return

		s_result['num'] = len(li)
		s_result['max'] =li[-1]
		s_result['min'] = li[0]
		s_result['sum_of_item'] = float(sum(li))
		sum_of_squares = sum(i**2 for i in li)
		s_result['avg'] = s_result['sum_of_item'] /  s_result['num']
		s_result['stdev'] = ((s_result['num'] * sum_of_squares - s_result['sum_of_item'] ** 2) / (s_result['num']**2))**0.5

		s_result['中位数'] = (li[s_result['num']/2] + li[s_result['num']/2 -1])/2.0 if s_result['num']%2 == 0 else li[s_result['num']/2]
		s_result['20'] = li[s_result['num']/5]
		s_result['40'] = li[s_result['num']/5*2]
		s_result['60'] = li[s_result['num']/5*3]
		s_result['80'] = li[s_result['num']/5*4]	
	
		return s_result

	@exeTime
	def get_anlyse(self,community,listfromDB):
		"""
		传入从数据库里查询出来的记录（由元组组成的列表）来进行数据分析
		"SELECT price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
	details_url,community_name FROM for_sale_property WHERE community_name LIKE '%%%s%%'"%comm
		"""
		if len(listfromDB) < 1:
			print("没有可供统计分析的数据")
			return

		#先把最高和最低的两个记录去掉，避免录入错误严重影响偏差。
		listfromDB = sorted(listfromDB, key=lambda x:x[0])
		num_list = len(listfromDB)

		print("\n****************** 最开始数据 ***********************")
		print("本次共有原始 %u个数据" %num_list)
		print("其价格区间为 %9.2f - %9.2F "%(listfromDB[0][0],listfromDB[-1][0]))

		# print("Now have %s datas"%num_list)
		if num_list < 20:
			print("这是个不活跃小区，数据少于20个,所以没有做去除工作")
		else:
			num_del = int(num_list / 200)
			if num_del < 2:	num_del = 2
			for i in range(0,num_del):
				del listfromDB[0]
				del listfromDB[-1]

		result = self.stat(zip(*listfromDB)[0])

		#把times个标准差之外的数据清除，生成一个新列表,理论上能覆盖近90%的数据
		times = 1.5 		#标准差的倍数
		times_stdev_top = times * result['stdev'] + result['avg']
		times_stdev_bottom = result['avg'] - times * result['stdev'] 
		new_li = []
		for i in listfromDB:
			if i[0] <= times_stdev_top and i[0] >= times_stdev_bottom:
				new_li.append(i)
		
		self.clear_datas = new_li
		new_result = self.stat(zip(*self.clear_datas)[0])

		print("\n****************** 初步清洗后数据 ***********************")
		print("本次共有原始 %u个数据" %(result['num']))
		print("其价格区间为 %9.2f - %9.2F "%(result['min'],result['max']))
		print("\n*************  覆盖" + community + "90% 数据分布情况 ************")
		self.pri_info(new_result)

		return result,new_result

		
	def pri_info(self,res):
		#输出数列的评估结果
		print("本次共有 %u个数据" %(res['num']))
		print("标准差为：%9.2f，标准差系统为：%5.2f %%"%(res['stdev'],res['stdev']/res['avg']*100))
		print("        0     **    20%    **    40%    **    60%    **    80%    **    100%    ")
		print("    %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f "%(res['min'],res['20'],res['40'],res['60'],res['80'],res['max']))
		print("中位数：%9.2f ,平均价: %9.2f"%(res['中位数'],res['avg']))
		print("评估价为 %9.2f ,价格区间 %9.2f - %9.2f"%(res['中位数']*0.82,res['中位数']*0.8,res['中位数']*0.90))
		print("总审价：%9.2f"%(res['60']))

	@exeTime
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

	@exeTime
	def out_enquiry(self,v2,comm_name,xj):
		if v2['stdev']/v2['avg']*100 >10:
			print("标准差系统过大，数据有效性不足")
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

		print(datetime.date.today(),comm_name,memo1,avg_floor,avg_t_floor,who,price,memo,year,struct,elevator)
		

		db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "apprsal",charset = "utf8")
		cursor = db.cursor()
		try:
			sql_equiry ="INSERT t_enquiry (Enquiry_Date,Enquiry_CellName,PA_Located,PA_Level,Apprsal_Use,Enquiry_PmName,\
				OfferPeople,Apprsal_Up,Enquiry_Source,Remark,Enquiry_Layout,PA_YearBuilt,PA_Structure,PA_Elevator)\
			                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql_equiry,(datetime.date.today(),comm_name,memo1,avg_floor,"住宅",who,"林晓",price,"估价师报价",memo,avg_t_floor,year,struct,elevator))
			db.commit()
		except:
			print("~~~ Wo，fault!!!~~~~~~")
		finally:
			cursor.close()
			db.close()

	@exeTime
	def queryBD(self):

		db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
		cursor = db.cursor()
		comm = "龙昌里"
		
		xjr = ""
		sql = "SELECT price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
		details_url,community_name FROM for_sale_property WHERE community_name LIKE '%%%s%%'"%comm

		cursor.execute(sql)
		
		datas = list(cursor.fetchall())

		cursor.close()
		db.close()
		# data_stat = DataStat()

		d = collections.Counter(zip(*datas)[10])
		# 瞬间出结果
		for k in d:
			print("%s : %s"%(k,d[k]))
		    # k是lst中的每个元素
		    # d[k]是k在lst中出现的次数

		if len(datas) == 0 :
			print("There is no datas in this community,check you community name and try again ......")
		else:
			v1,v2 = data_stat.get_anlyse(comm,datas)

			avg_area = int(sum(i[1] for i in data_stat.clear_datas))/len(data_stat.clear_datas)
			floor_datas_num = 0
			floor_datss_sum = 0
			for i in data_stat.clear_datas:
				if i[2] > 0:
					floor_datss_sum += int(i[2])
					floor_datas_num += 1
			avg_floor = floor_datss_sum / floor_datas_num
			print("平均面积为 %6.0f"%(avg_area))
			print("平均楼层为 %6.0f"%(avg_floor))
			
			# if xjr:
			# 	data_stat.out_enquiry(v2,comm,xjr)


	# plt.plot(zip(*data_stat.clear_datas)[0],zip(*data_stat.clear_datas)[1],'o')
	# plt.show()
if __name__=="__main__":
	data_stat = DataStat()
	data_stat.queryBD()
			







