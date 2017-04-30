#coding:utf-8
# 把excel内的案例数据输入到数据库中去
import MySQLdb
import xlrd
import datetime

db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "apprsal_cdh",charset = "utf8")
cursor = db.cursor()

data = xlrd.open_workbook('case_report(2015-11-01--2015-11-30).xls')
table = data.sheets()[0]   
nrows = table.nrows
ncols = table.ncols
sql_equiry ="INSERT t_case_cfg (Case_Name,Case_Located,Case_Region,Case_Type,Case_TrxDate,Case_Trx,\
		Case_TrxPrice,Case_Area,Case_Structure,Case_Function,Case_Towards,Case_Level,Case_Cmpl_Years,Case_Decoration,\
		Case_Elevator,Case_trafficBase,Case_road,Case_Facilities,Case_EQ,Case_Image,Opertor,opert_time,case_Payment)\
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sus = 0
dupli = 0
for i in range(1,nrows):
	a = table.cell(i,4).value.replace('.0','')

	b = datetime.datetime.strptime(str(a), "%Y-%m-%d %H:%M:%S").date()
	img = table.cell(i,19).value.replace('E://','D://')

	try:
		cursor.execute(sql_equiry,(table.cell(i,0).value,table.cell(i,1).value,table.cell(i,2).value,table.cell(i,3).value,b,table.cell(i,5).value\
			,table.cell(i,6).value,table.cell(i,7).value,table.cell(i,8).value,table.cell(i,9).value,table.cell(i,10).value,table.cell(i,11).value,table.cell(i,12).value\
			,table.cell(i,13).value,table.cell(i,14).value,table.cell(i,15).value,table.cell(i,16).value,table.cell(i,17).value,table.cell(i,18).value,img
			,table.cell(i,20).value,table.cell(i,21).value,1))
		db.commit()
		sus += 1
		print "input sucess " + str(sus)
	except MySQLdb.Error,e:
		if e.args[0] == 1062 :
			dupli = dupli + 1
			print "dupli " + str(dupli)
		print i
		print e




	# try:		
	# 	cursor.execute(sql_equiry,(datetime.date.today(),comm_name,memo1,avg_floor,"住宅",who,"林晓",price,"估价师报价",memo,avg_t_floor,year,struct,elevator))
	# 	db.commit()
		# for j in range(ncols):
		# print table.cell(i,j).value
	# for j in range(22):
	# 	print j,table.cell(i,j).value

	# print "*"*50
db.close()