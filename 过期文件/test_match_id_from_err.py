# coding:utf-8
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf-8")

#直接从生成出错的表里重新解析生成id

# 从excel表格中读出并生成小区列表
import xlrd
data = xlrd.open_workbook('comm.xlsx')
table = data.sheet_by_name(u'Sheet3')
nrows = table.nrows
ncols = table.ncols

comm_arr = []
for row in range(1,nrows):
	for col in range(7,ncols):			#这个循环是，如果小区名有别名，把它们分拆成不同的元素加入字典
		comm = table.row(row)[col].value.encode("utf8")
		if comm.strip() != '':
			k_v = []
			k_v.append(int(table.row(row)[5].value))
			k_v.append(comm)
			comm_arr.append(k_v)	#每个元素	0：小区id,1：小区关键字


db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
cursor = db.cursor()	


# sql = "SELECT id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
		# details_url,community_name,first_acquisition_time,from_ FROM for_sale_property ORDER BY id LIMIT " + str(n) + "," + str(step)

sql = "SELECT for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_ FROM for_sale_err"

cursor.execute(sql)
# datas = list(cursor.fetchall())
datas = cursor.fetchall()
k = 0
dupli = 1
for data in datas:

	str1 = data[11].replace("·","").replace(".","").encode("utf8").upper().strip()

	getid = []					#存放匹配成功的小区关键字
	for i in comm_arr:								#小区关键字列表来轮询
		key_words = i[1].split("/")					#对带“/”的关键字进行拆分，第一个是关键字，后面是补充区分的
		start = str1.find(key_words[0].upper())			#在community_name(data[11])中查找关键字key_words[0],key_words其他元素是辅助
		if start >= 0:
			lenth=len(key_words)					#对于关键字中有"/"的关键字，要继续用其他关键字进一步匹配
			if lenth > 1:
				formatch = str1 + data[4].encode("utf8").upper()				#把title+community_name相加成一个匹配字段
				for j in range(1,lenth):
					if formatch.find(key_words[j].upper()) >=0:		#用data[4]title进行匹配
						# temp = [start,i[1],i[0]]			#只要匹配到一个即可，退出循环
						temp = [start,key_words[0].upper(),i[0]]
						getid.append(temp)
						break
			else:
				temp = [start,key_words[0].upper(),i[0]]			#对于关键字中没有“/”的，匹配成功就可以了
				getid.append(temp)

	try:
		if len(getid) == 1:
			sql_del = "delete from for_sale_err where for_sale_property_id = " + str(data[0])
			cursor.execute(sql_del)
			db.commit()
			sql_insert ="INSERT for_sale (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],getid[0][2]))
			db.commit()

		elif len(getid) == 0:
			# sql_insert ="INSERT for_sale_err (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
			# 	details_url,community_name,first_acquisition_time,from_) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			# cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13]))
			# db.commit()
			print(str(k)+"---------nofind")
		elif len(getid) > 1:
			flag = False
			getid.sort(key=lambda x:x[0]) 			#按照匹配关键字的位置排序，先匹配到的排在前面		
			first = getid[0]
			get = str(getid[0][0]) +',' + str(getid[0][1]) +',' + str(getid[0][2]) + "/"
			
			for l in range(1,len(getid)):
				if(getid[l][0] > first[0]):			#当有多个小区名称被匹配成功时，以第一个为准
					break
				else:								#如果有并列第一：
					if len(getid[l][1]) > len(first[1]):		#字符串长的优先
						first = getid[l]
					elif len(getid[l][1]) == len(first[1]):		#字符串相同的，要人工判断一下
						get += str(getid[l][0]) +',' + str(getid[l][1]) +',' + str(getid[l][2]) + "/"
						flag = True
			if flag:
				sql_insert ="INSERT for_sale_mul (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
							details_url,community_name,first_acquisition_time,from_,getid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],get))
				db.commit()
				print(str(k)+"---------mul")
			else:
				sql_del = "delete from for_sale_err where for_sale_property_id = " + str(data[0])
				cursor.execute(sql_del)
				db.commit()
				sql_insert ="INSERT for_sale (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],first[2]))
				db.commit()
				
			
			#下面一段是把所有匹配多关键字的记录下来检查
			print(str(k)+"---------mul----for checked")
			get1 = ""
			f1 = False
			a = getid[0][2]
			for item in getid:
				print(str(item[0]) + "," + item[1] + "," + str(item[2]))
				if item[2] != a:			#如果虽然匹配成功多个小区关键字，可是小区id是一样的，忽略
					f1 = True
				get1 += str(item[0]) + "," + item[1] + "," + str(item[2]) + "|"

			if f1:
				try:
					sql_insert ="INSERT for_sale_mul_check (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
									details_url,community_name,first_acquisition_time,from_,getid,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],\
						data[9],data[10],data[11],data[12],data[13],get1,first[2]))
					db.commit()
				except MySQLdb.Error,e:
					pass
		k = k + 1

	except MySQLdb.Error,e:
		if e.args[0] == 1062 :
			print(str(dupli)+"aready have")
			dupli = dupli + 1



cursor.close()
db.close()