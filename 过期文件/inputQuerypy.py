#coding:utf-8
# 把excel内的询价数据输入到数据库中去
import MySQLdb
import xlrd
import datetime

db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "apprsal_cdh",charset = "utf8")
cursor = db.cursor()

data = xlrd.open_workbook('201512.xls')
table = data.sheets()[0]   
nrows = table.nrows
# ncols = table.ncols
sql_equiry ="INSERT t_enquiry (Enquiry_Date,Enquiry_CellName,PA_Located,PA_Level,Apprsal_Use,Enquiry_PmName,\
				OfferPeople,Apprsal_Up,Enquiry_Source,Remark,Enquiry_Layout,PA_YearBuilt,PA_Structure,PA_Elevator)\
			                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sus = 0
dupli = 0
for i in range(1,nrows):
	a = table.cell(i,0).value.replace('.0','')
	# print a
	b = datetime.datetime.strptime(a.encode('utf-8'), "%Y-%m-%d %H:%M:%S").date()

	year = table.cell(i,6).value.replace('.0','')
	if year == '':
		new_year = None
	else:
		new_year = datetime.datetime.strptime(year.encode('utf-8'), "%Y-%m-%d %H:%M:%S").date()

	# img = table.cell(i,19).value.replace('E://','D://')

	# try:
	cursor.execute(sql_equiry,(b,table.cell(i,1).value,table.cell(i,2).value,table.cell(i,4).value,table.cell(i,5).value\
		,table.cell(i,10).value,table.cell(i,11).value,table.cell(i,9).value,table.cell(i,12).value,table.cell(i,13).value,table.cell(i,3).value,new_year\
		,table.cell(i,7).value,table.cell(i,8).value))
	db.commit()
	sus += 1
	print "input sucess " + str(sus)


db.close()