# coding:utf-8
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf-8")


with open('5.txt') as f:
	comm_arr = []
	s = f.readlines() 
	for line in s:  
		line = line.replace("\n","").encode('utf-8')
		l = line.split("\t")
		for j in range(2,6):			#这个循环是，如果小区名有别名，把它们分拆成不同的元素加入字典
			if l[j].strip() != '':
				k_v = []
				k_v.append(l[0])
				k_v.append(l[j])
				comm_arr.append(k_v)	#每个元素	0：小区id,1：小区关键字


db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
cursor = db.cursor()	

n = 0
step = 2000

sql = "SELECT id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
		details_url,community_name,first_acquisition_time,from_ FROM for_sale_property ORDER BY id LIMIT " + str(n) + "," + str(n+step)

cursor.execute(sql)
# datas = list(cursor.fetchall())
datas = cursor.fetchall()
k = 0
dupli = 1
for data in datas:

	str1 = data[11].replace("·","")

	getid = []
	for i in comm_arr:								#小区关键字列表来轮询
		key_words = i[1].split("/")					#对带“/”的关键字进行拆分，第一个是关键字，后面是补充区分的
		start = str1.find(key_words[0])			#先用小区名称data[11]进行关键字匹配
		if start >= 0:
			lenth=len(key_words)					#对于关键字中有"/"的关键字，要继续用其他关键字进一步匹配
			if lenth > 1:
				formatch = str1 + data[4]				#把title+community_name相加成一个匹配字段
				for j in range(1,lenth):
					if formatch.find(key_words[j]) >=0:		#用data[4]title进行匹配
						temp = [start,i[1],i[0]]			#匹配成功，就可以进入匹配成功列表，退出循环
						getid.append(temp)
						break
			else:
				temp = [start,i[1],i[0]]			#对于关键字中没有“/”的，匹配成功就可以了
				getid.append(temp)

	try:
		if len(getid) == 1:
			sql_insert ="INSERT for_sale (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],getid[0][2]))
			db.commit()
			print(str(k)+"---------ok")

		elif len(getid) == 0:
			sql_insert ="INSERT for_sale_err (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13]))
			db.commit()
			print(str(k)+"---------nofind")

		elif len(getid) > 1:
			flag = False

			getid.sort(key=lambda x:x[0]) 
			first = getid[0]
			get = str(getid[0][0]) +',' + getid[0][1] +',' + getid[0][2] + "/"
			
			for l in range(1,len(getid)):
				if(getid[l][0] > first[0]):
					break
				else:
					if len(getid[l][1]) > len(first[1]):
						first = getid[l]
					else:
						get += str(getid[0][0]) +',' + getid[0][1] +',' + getid[0][2] + "/"
						flag = True

			if flag:
				sql_insert ="INSERT for_sale_mul (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
							details_url,community_name,first_acquisition_time,from_,getid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],get))
				db.commit()
				print(str(k)+"---------mul")
			else:
				sql_insert ="INSERT for_sale (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],getid[0][2]))
				db.commit()
				print(str(k)+"---------ok")

		k = k + 1

	except MySQLdb.Error,e:
		if e.args[0] == 1062 :
			print(str(dupli)+"aready have")
			dupli = dupli + 1

# print(len(getid))
		


# for i in getid:
# 	print str(i[0]) +',' + i[1] +',' + i[2]

cursor.close()
db.close()