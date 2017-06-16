#coding:utf-8
# 通过数据库查询记录，并可记录到询价数据库中
from __future__ import print_function
from spider import html_outputer,mytools
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


class DataStat(object):
	"""
	这是一个分析由元组组成的列表的类
	输入列表
	输出分析结果的列表
	输出含分析结果的字符串
	"""

	def __init__(self):
		self.final_data = []				#存放传入的数据
		self.info = ''
		self.xjr = { 
			"hyx":"黄燕翔","jq":"贾琴","jz":"金忠","lyx":"廖亚香","czy":"陈志艳","xz":"项争","cyw":"陈玉炜","gs":"公司外部","kc":"柯琛",
			"lmc":"林美彩","clh":"陈丽华","wml":"吴木兰","cym":"陈幼梅","cjy":"陈军勇","zly":"朱黎英","wj":"吴洁","wlt":"伍灵婷"
			}
		self.datas = []


	def stat(self,li,stamp):
		
		# 数据分析,
		# li：传入的列表,
		# stamp：相应的标记，这样返回的字典的key可以不一样

		s_result = {}
		if len(li) < 1:
			pri_info("没有可供统计分析的数据")
			return

		s_result[stamp + 'len'] = len(li)
		s_result[stamp + 'max'] =li[-1]
		s_result[stamp + 'min' ] = li[0]
		s_result[stamp + 'sum'] = float(sum(li))
		sum_of_squares = sum(i**2 for i in li)
		s_result[stamp + 'avg'] = s_result[stamp + 'sum' ] /  s_result[stamp + 'len' ]
		s_result[stamp + 'stdev'] = ((s_result[stamp + 'len'] * sum_of_squares - s_result[stamp + 'sum'] ** 2) / (s_result[stamp + 'len' ]**2))**0.5
		s_result[stamp + '中位数' ] = (li[s_result[stamp + 'len']/2] + li[s_result[stamp + 'len']/2 -1])/2.0 \
							if s_result[stamp + 'len' ]%2 == 0 else li[s_result[stamp + 'len' ]/2]
		s_result[stamp + '20' ] = li[s_result[stamp + 'len']/5]
		s_result[stamp + '40'] = li[s_result[stamp + 'len']/5*2]
		s_result[stamp + '60' ] = li[s_result[stamp + 'len']/5*3]
		s_result[stamp + '80'] = li[s_result[stamp + 'len' ]/5*4]	
	
		return s_result

	@mytools.exeTime
	def get_anlyse(self,community,listfromDB):
		"""
		传入从数据库里查询出来的记录（由元组组成的列表）来进行数据分析
		"SELECT price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
	details_url,community_name FROM for_sale_property WHERE community_name LIKE '%%%s%%'"%comm
		"""
				
		if len(listfromDB) < 1:
			self.info = self.info + "没有可供统计分析的数据"
			return

		resu = {}			#2016.5.27存放分析结果的字典

		resu['comm'] = community

		# 如果是从数据库里查询出来的记录，是由元组组成的list;
		# 如果直接从网上抓的，是由字典组成的list，需要分别处理

		listfromDB = sorted(listfromDB, key=lambda x:x['price']) if isinstance(listfromDB[0],dict) else sorted(listfromDB, key=lambda x:x[0])
		# 这是最原始的数据
		resu['original_len'] = len(listfromDB)  
		resu['original_min'] = listfromDB[0]['price'] if isinstance(listfromDB[0],dict) else listfromDB[0][0] 
		resu['original_max'] = listfromDB[-1]['price'] if isinstance(listfromDB[0],dict) else listfromDB[-1][0]

				
		#初步清洗：先把最高和最低的0.5%记录去掉，避免因为录入错误严重影响偏差。
		if resu['original_len'] >= 20:
			num_del = int(resu['original_len'] / 200)			
			if num_del < 2:	num_del = 2
			for i in range(0,num_del):
				del listfromDB[-1]
				del listfromDB[0]
		
		# 这时的listfromDB已经去掉了“最高分”和“最低分”
		result = self.stat([i['price'] for i in listfromDB],'clear_') if isinstance(listfromDB[0],dict) else self.stat(zip(*listfromDB)[0],'clear_')
		resu = dict(resu,**result)

		#把times个标准差之外的数据清除，生成一个新列表,理论上能覆盖近90%的数据
		times = 1.5 		#标准差的倍数
		times_stdev_top = times * resu['clear_stdev'] + resu['clear_avg']
		times_stdev_bottom = resu['clear_avg'] - times * resu['clear_stdev'] 
		self.final_data = []
		for i in listfromDB:
			temp = i['price'] if isinstance(listfromDB[0],dict) else i[0]
			if temp <= times_stdev_top and temp >= times_stdev_bottom:
				self.final_data.append(i)
		
		
		# self.final_data是统计意义内的数据
		final_result = self.stat([i['price'] for i in self.final_data],'final_') if isinstance(listfromDB[0],dict) else self.stat(zip(*self.final_data)[0],'final_')
		resu = dict(resu,**final_result)
		
		resu['final_area_avg'] = int(sum(i['area'] for i in self.final_data))/len(self.final_data) \
						if isinstance(listfromDB[0],dict) else int(sum(i[1] for i in self.final_data))/len(self.final_data)
		floor_datas_num = 0
		floor_datss_sum = 0
		year_sum = 0
		year_num = 0
		t_floor_sum = 0
		t_floor_nmu = 0


		for i in self.final_data:
			floor_index = i['floor_index'] if isinstance(listfromDB[0],dict) else i[2]
			if floor_index > 0:
				floor_datss_sum += floor_index
				floor_datas_num += 1
			
			year = i['builded_year'] if isinstance(listfromDB[0],dict) else i[6]
			if year > 1800:
				year_sum += year
				year_num += 1

			t_floor = i['total_floor'] if isinstance(listfromDB[0],dict) else i[5]
			if t_floor > 0:
				t_floor_sum += t_floor
				t_floor_nmu += 1

		resu['final_floor_avg'] = floor_datss_sum / floor_datas_num if floor_datas_num > 0 else 0       #2016.5.29避免除0错误
		resu['final_tfloor_avg'] = t_floor_sum / t_floor_nmu if t_floor_nmu > 0 else 0
		resu['final_year_avg'] = year_sum / year_num if year_num > 0 else 0
		self.pri_info(resu)

		return resu

		
	def pri_info(self,res):
		#输出数列的评估结果
		self.info = ''
		self.info = self.info + "****************** 原始数据 ***********************"
		self.info = self.info + "\n本次共有原始 %u个数据" %res['original_len']
		self.info = self.info + "\n其价格区间为 %9.2f - %9.2F "%(res['original_min'],res['original_max'])

		if res['original_len'] < 20:
			self.info = self.info + "\n这是个不活跃小区，数据少于20个,所以没有做去除工作"

		self.info = self.info + "\n****************** 初步清洗后数据 ***********************"
		self.info = self.info + "\n去除高低值后还有 %u个数据" %(res['clear_len'])
		self.info = self.info + "\n其价格区间为 %9.2f - %9.2F "%(res['clear_min'],res['clear_max'])

		self.info = self.info + "\n************* " + res['comm'] + " : 90% 有效数据分布情况 ************"
		self.info = self.info + "\n本次共有 %u个数据" %(res['final_len'])
		self.info = self.info + "\n标准差为：%9.2f，标准差系统为：%5.2f %%"%(res['final_stdev'],res['final_stdev']/res['final_avg']*100)
		self.info = self.info + "\n        0     **    20%    **    40%    **    60%    **    80%    **    100%    "
		self.info = self.info + "\n    %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f ** %9.2f "\
					%(res['final_min'],res['final_20'],res['final_40'],res['final_60'],res['final_80'],res['final_max'])
		self.info = self.info + "\n中位数：%9.2f ,平均价: %9.2f"%(res['final_中位数'],res['final_avg'])
		self.info = self.info + "\n评估价为 %9.2f ,价格区间 %9.2f - %9.2f"%(res['final_中位数']*0.82,res['final_中位数']*0.8,res['final_中位数']*0.90)
		self.info = self.info + "\n总审价：%9.0f"%(res['final_60'])

		self.info = self.info + "\n平均面积为 %6.0f"%(res['final_area_avg'] )
		self.info = self.info + "\n平均楼层为 %6.0f"%(res['final_floor_avg'])
		self.info = self.info + "\n平均总楼层 %6.0f"%(res['final_tfloor_avg'] )
		self.info = self.info + "\n建成年份 %8.0f"%(res['final_year_avg'])

	@mytools.exeTime
	def out_xlsx(self,keywords):
		try:
			outputer = html_outputer.HtmlOutputer()
			outputer.datas = self.datas
			outputer.out_xlsx(keywords,'SQL')
		except Exception as e:
			with open('log.txt','a+') as fout:
				fout.write(str(datetime.datetime.now()) + '\n')
				traceback.print_exc(file=fout) 
				traceback.print_exc
		return keywords.decode() + 'SQL.xlsx'



	@mytools.exeTime
	def out_enquiry(self,resu,xj):			#2016.6.2传入的参数不再需要comm
		
		now = datetime.date.today()
		month_ago = now - datetime.timedelta(30)
		offer = "林晓"
		
		
		db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "apprsal_cdh",charset = "utf8")
		cursor = db.cursor()

		try:
			# 2016.6.2增加了避免重复报价的功能
			sql1 = "SELECT COUNT(Enquiry_CellName) FROM t_enquiry WHERE Enquiry_CellName = '%s' AND Enquiry_Date > '%s' AND OfferPeople = '%s'"%(resu['comm'],month_ago,offer)
			cursor.execute(sql1)
			num = cursor.fetchall()[0][0]
			if num >= 1:
				print('There already have record in 30 days')
			else:
				who = self.xjr[xj]
				avg_t_floor = resu['final_tfloor_avg'] 		#2016.5.30直接用get_analyse中的数据
				avg_b_year = resu['final_year_avg'] 
				year = str(avg_b_year) + "-01-01 00:00:00"
				price = int(resu['final_中位数']*0.82)
				memo = "%s个数据，挂牌区间%.0f-%.0f"%(resu['final_len'],resu['final_min'],resu['final_80'])
				elevator = "带电梯" if avg_t_floor > 8 else "无电梯"
				struct = "钢混结构" if avg_t_floor > 7 else "砖混结构"
				memo1 = "二手房评估可以%.0f"%(round(float(resu['final_20'])/100,0)*100)
				if resu['final_stdev']/resu['final_avg']*100 >10:memo1 = memo1 + ", 但标准差系数达%.2f,数据可靠性不足"%(resu['final_stdev']/resu['final_avg']*100)
				ResultString = '%s,%s,%s,%.0f,%.0f,%s,%.2f,%s,%s,%s,%s'%(datetime.date.today(),resu['comm'],memo1,resu['final_floor_avg'],avg_t_floor,who,price,memo,year,struct,elevator)
				mytools.pri(ResultString)
				sql_equiry ="INSERT t_enquiry (Enquiry_Date,Enquiry_CellName,PA_Located,PA_Level,Apprsal_Use,Enquiry_PmName,\
							OfferPeople,Apprsal_Up,Enquiry_Source,Remark,Enquiry_Layout,PA_YearBuilt,PA_Structure,PA_Elevator)\
						                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql_equiry,(datetime.date.today(),resu['comm'],memo1,resu['final_floor_avg'],"住宅",who,"林晓",price,"估价师报价",memo,avg_t_floor,year,struct,elevator))
				db.commit()
		except Exception as e:
			print("~~~ Wo，fault!!!~~~~~~")
			with open('log.txt','a+') as fout:
				fout.write(str(datetime.datetime.now()) + '\n')
				traceback.print_exc(file=fout) 
				traceback.print_exc
		finally:
			cursor.close()
			db.close()

	@mytools.exeTime
	def query_main(self, comm, xjr = ''):

		'''直接从数据库里查询询价记录'''
		
		db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
		cursor = db.cursor()

		sql = "SELECT a.* FROM (SELECT price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
		details_url,community_name FROM for_sale_property FORCE INDEX (date_index) ORDER BY first_acquisition_time DESC LIMIT 0,300000) \
		as a WHERE community_name like '%%%s%%'"%(comm)

		cursor.execute(sql)
		self.datas = list(cursor.fetchall())
		cursor.close()
		db.close()

		info = ''

		if len(self.datas) == 0 :
				info = info + "There is no datas in this community,check you community name and try again ......"
				v2 = ''
		else:
			
			self.d = collections.Counter(zip(*self.datas)[10])
			# for k in self.d:
			# 	info = info + "%s : %s\n"%(k,self.d[k])
			    # k是lst中的每个元素
			    # d[k]是k在lst中出现的次数
			v2 = self.get_anlyse(comm,self.datas)
			info = info + self.info

		return info,v2

	def query_again_by_area_or_totalfloor(self,area_list = [],tfloor_list = []):
		if len(self.datas) == 0:
			print("query datas first .....")
			return
		if len(area_list) > 0 :
			query_again_by_area = []
			for item in self.datas:
				if item[1] in area_list:
					query_again_by_area.append(item)

		return query_again_by_area


if __name__=="__main__":

	comm = "慧景"
	xjr = ""
	
	data_stat = DataStat()
	info,v2 = data_stat.query_main(comm,xjr)




	print(info)
	
	if xjr:
		data_stat.out_enquiry(v2,xjr)
	


			







