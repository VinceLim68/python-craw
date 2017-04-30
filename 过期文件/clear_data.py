#-*- coding:utf-8 -*-
from __future__ import print_function
import MySQLdb


db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
cursor = db.cursor()
num = 0 
i = 0
j = 0
k = 0
# sql1 = "SELECT title,area,spatial_arrangement,price,floor_index,total_floor,builded_year,advantage,\
# 	total_price,details_url,community_name,first_acquisition_time,from_,id FROM for_sale_property order by id limit %d,100000"%(num)
# cursor.execute(sql1)
# raw_datas = cursor.fetchall()
# print(len(raw_datas))
while True:
	sql1 = "SELECT title,area,spatial_arrangement,price,floor_index,total_floor,builded_year,advantage,\
	total_price,details_url,community_name,first_acquisition_time,from_,id FROM for_sale_property order by id limit %d,100000"%(num)
	cursor.execute(sql1)
	raw_datas = cursor.fetchall()
	num = num + 100000
	if len(raw_datas) <= 0:
		break


	for data in raw_datas:
		data1 = list(data)
		data1[5] = filter(str.isdigit,str(data[5]).encode("utf8"))
		data1[6] = filter(str.isdigit,str(data[6]).encode("utf8"))
		data1[10] = data[10].strip()
		


		try:
			update_sql = """UPDATE for_sale_property SET community_name = %s ,total_floor = %s ,builded_year = %s where id = %s"""
			cursor.execute(update_sql,(data1[10],data1[5],data1[6],data1[13]))
			db.commit()
			i += 1
			# print("save %s"%(i))
		except MySQLdb.Error,e:
			if e.args[0] == 1062 :
				del_sql = "DELETE from for_sale_property where id = %s"
				cursor.execute(del_sql,data1[13])
				db.commit()
				j += 1
				# print ("discard %s"%(j))
		k += 1
		if k == 1000:
			print("save %s, discard %s"%(i,j))
			k=0


cursor.close()
db.close()
