#coding:utf-8

from __future__ import print_function
import MySQLdb
import datetime
import matplotlib.pyplot as plt
# def out_enquiry(self,resu,xj):			#2016.6.2传入的参数不再需要comm
		
now = datetime.date.today()
n1 = (now - datetime.timedelta(30))
comm = u"中航城1"
offer = u"林晓"
print(n1)
# print(pre)
		# who = self.xjr[xj]
		# avg_t_floor = resu['final_tfloor_avg'] 		#2016.5.30直接用get_analyse中的数据
		# avg_b_year = resu['final_year_avg'] 
		# year = str(avg_b_year) + "-01-01 00:00:00"
		# price = int(resu['final_中位数']*0.82)
		# memo = "%s个数据，挂牌区间%.0f-%.0f"%(resu['final_len'],resu['final_min'],resu['final_80'])
		# elevator = "带电梯" if avg_t_floor > 8 else "无电梯"
		# struct = "钢混结构" if avg_t_floor > 7 else "砖混结构"
		# memo1 = "二手房评估可以%.0f"%(round(float(resu['final_20'])/100,0)*100)
		# if resu['final_stdev']/resu['final_avg']*100 >10:memo1 = memo1 + ", 但标准差系数达%.2f,数据可靠性不足"%(resu['final_stdev']/resu['final_avg']*100)
		# print(datetime.date.today(),resu['comm'],memo1,resu['final_floor_avg'],avg_t_floor,who,price,memo,year,struct,elevator)
		
db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "apprsal",charset = "utf8")
cursor = db.cursor()
sql1 = "select COUNT(Enquiry_CellName) from t_enquiry WHERE Enquiry_CellName = '%s' AND Enquiry_Date > '%s' AND OfferPeople = '%s'"%(comm,n1,offer)
cursor.execute(sql1)
num = cursor.fetchall()[0][0]
if num >= 1 :
	print(">=1")
else:
	print("=0")
# print(num)
cursor.close()
db.close()
		# try:
		# 	sql_equiry ="INSERT t_enquiry (Enquiry_Date,Enquiry_CellName,PA_Located,PA_Level,Apprsal_Use,Enquiry_PmName,\
		# 		OfferPeople,Apprsal_Up,Enquiry_Source,Remark,Enquiry_Layout,PA_YearBuilt,PA_Structure,PA_Elevator)\
		# 	                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		# 	cursor.execute(sql_equiry,(datetime.date.today(),resu['comm'],memo1,resu['final_floor_avg'],"住宅",who,"林晓",price,"估价师报价",memo,avg_t_floor,year,struct,elevator))
		# 	db.commit()
		# except Exception as e:
		# 	print("~~~ Wo，fault!!!~~~~~~")
		# 	with open('log.txt','a+') as fout:
		# 		fout.write(str(datetime.datetime.now()) + '\n')
		# 		traceback.print_exc(file=fout) 
		# 		traceback.print_exc
		# finally:
		# 	cursor.close()
		# 	db.close()

