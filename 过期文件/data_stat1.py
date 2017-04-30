#coding:utf-8
# 通过数据库查询记录，并可记录到询价数据库中
from __future__ import print_function
from spider import html_outputer
import MySQLdb
import sys
import xlsxwriter
import datetime
import time
import collections
import traceback 
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
	"""
	这是一个分析由元组组成的列表的类
	输入列表
	输出分析结果的列表
	输出含分析结果的字符串
	"""

	def __init__(self):
		self.clear_datas = []				#存放传入的数据
		self.info = ''
		self.xjr = { 
			"hyx":"黄燕翔","jq":"贾琴","jz":"金忠","lyx":"廖亚香","czy":"陈志艳","xz":"项争","cyw":"陈玉炜","gs":"公司外部","kc":"柯琛",
			"lmc":"林美彩","clh":"陈丽华","wml":"吴木兰","cym":"陈幼梅","cjy":"陈军勇","zly":"朱黎英","wj":"吴洁","wlt":"伍灵婷"
			}


	def stat(self,li):
		#传入查询的出来的记录：多维列表,keyindex表示分析的是第几个元素（从0开始）
		s_result = {}
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
		self.info = ''
		if len(listfromDB) < 1:
			self.info = self.info + "没有可供统计分析的数据"
			return

		#先把最高和最低的两个记录去掉，避免录入错误严重影响偏差。

		#如果是从数据库里查询出来的记录，是由元组组成的list;如果直接从网上抓的，是由字典组成的list，需要分别处理
		if isinstance(listfromDB[0],dict):
			dictlist = listfromDB
			listfromDB = []
			for data in dictlist:
				item = []
				item.append(data['price'] if data.has_key('price') else 0)
				item.append(data['area'] if data.has_key('area') else 0)
				item.append(data['floor_index'] if data.has_key('floor_index') else 0)
				item.append(data['title'] if data.has_key('title') else '')
				item.append(data['spatial_arrangement'] if data.has_key('spatial_arrangement') else '')
				item.append(data['total_floor'] if data.has_key('total_floor') else 0)
				item.append(data['builded_year'] if data.has_key('builded_year') else 0)
				item.append(data['advantage'] if data.has_key('advantage') else '')
				item.append(data['total_price'] if data.has_key('total_price') else 0)
				item.append(data['details_url'] if data.has_key('details_url') else '')
				item.append(data['community_name'].strip() if data.has_key('community_name') else '')
				listfromDB.append(item)
             

		
		listfromDB = sorted(listfromDB, key=lambda x:x[0])

		num_list = len(listfromDB)

		self.info = self.info + "\n****************** 最开始数据 ***********************"
		self.info = self.info + "\n本次共有原始 %u个数据" %num_list
		self.info = self.info + "\n其价格区间为 %9.2f - %9.2F "%(listfromDB[0][0],listfromDB[-1][0])

		if num_list < 20:
			self.info = self.info + "\n这是个不活跃小区，数据少于20个,所以没有做去除工作"
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
			temp = i['price'] if isinstance(listfromDB[0],dict) else i[0]
			if temp <= times_stdev_top and temp >= times_stdev_bottom:
				new_li.append(i)
		
		self.clear_datas = new_li
		new_result = self.stat(zip(*self.clear_datas)['price']) if isinstance(self.clear_datas[0],dict) else self.stat(zip(*self.clear_datas)[0])

		self.info = self.info + "\n****************** 初步清洗后数据 ***********************"
		self.info = self.info + "\n本次共有原始 %u个数据" %(result['num'])
		self.info = self.info + "\n其价格区间为 %9.2f - %9.2F "%(result['min'],result['max'])
		self.info = self.info + "\n*************  覆盖" + community + "90% 数据分布情况 ************"
		self.pri_info(new_result)

		return result,new_result

		
	def pri_info(self,res):
		#输出数列的评估结果
		self.info = self.info + "\n本次共有 %u个数据" %(res['num'])
		self.info = self.info + "\n标准差为：%9.2f，标准差系统为：%5.2f %%"%(res['stdev'],res['stdev']/res['avg']*100)
		self.info = self.info + "\n        0     **    20%    **    40%    **    60%    **    80%    **    100%    "
		self.info = self.info + "\n    %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f "%(res['min'],res['20'],res['40'],res['60'],res['80'],res['max'])
		self.info = self.info + "\n中位数：%9.2f ,平均价: %9.2f"%(res['中位数'],res['avg'])
		self.info = self.info + "\n评估价为 %9.2f ,价格区间 %9.2f - %9.2f"%(res['中位数']*0.82,res['中位数']*0.8,res['中位数']*0.90)
		self.info = self.info + "\n总审价：%9.2f"%(res['60'])

	@exeTime
	def out_xlsx(self,keywords,datas):
		outputer = html_outputer.HtmlOutputer()
		outputer.datas = datas
		outputer.out_xlsx(keywords,'SQL')


	@exeTime
	def out_enquiry(self,v2,comm_name,xj):
		if v2['stdev']/v2['avg']*100 >10:
			print("\n标准差系统过大，数据有效性不足")
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

	# def query_main(self,comm):
		


if __name__=="__main__":
	db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
	cursor = db.cursor()
	comm = "金祥大厦"
	
	xjr = ""
	sql = "SELECT price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
	details_url,community_name FROM for_sale_property WHERE community_name LIKE '%%%s%%'"%comm

	cursor.execute(sql)
	
	datas = list(cursor.fetchall())

	cursor.close()
	db.close()

	info = ''
	data_stat = DataStat()

	if len(datas) == 0 :
		info = info + "There is no datas in this community,check you community name and try again ......"
	else:
		
		d = collections.Counter(zip(*datas)[10])
		for k in d:
			info = info + "%s : %s\n"%(k,d[k])
		    # k是lst中的每个元素
		    # d[k]是k在lst中出现的次数
		v1,v2 = data_stat.get_anlyse(comm,datas)
		info = info + data_stat.info
		try:
			data_stat.out_xlsx(comm,datas)
		except Exception, e:
			with open('log.txt','a+') as fout:
				fout.write(str(datetime.datetime.now()) + '\n')
				traceback.print_exc(file=fout) 
				traceback.print_exc()
		avg_area = int(sum(i[1] for i in data_stat.clear_datas))/len(data_stat.clear_datas)
		floor_datas_num = 0
		floor_datss_sum = 0
		for i in data_stat.clear_datas:
			if i[2] > 0:
				floor_datss_sum += int(i[2])
				floor_datas_num += 1
		avg_floor = floor_datss_sum / floor_datas_num
		info = info + "\n平均面积为 %6.0f"%(avg_area)
		info = info + "\n平均楼层为 %6.0f"%(avg_floor)
		print(info)
		if xjr:
			data_stat.out_enquiry(v2,comm,xjr)


	# plt.plot(zip(*data_stat.clear_datas)[0],zip(*data_stat.clear_datas)[1],'o')
	# plt.show()

			







