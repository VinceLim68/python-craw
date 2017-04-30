# coding:utf-8
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf-8")

# 从excel表格中读出并生成小区列表
import xlrd
data = xlrd.open_workbook('comm.xlsx')
table2 = data.sheet_by_name(u'Sheet1')
nrows2 = table2.nrows
ncols2 = table2.ncols

road_arr = []
for row in range(1,nrows2):
	for col in range(7,ncols2):			#这个循环是，如果小区名有别名，把它们分拆成不同的元素加入字典
		comm = table2.row(row)[col].value.encode("utf8")
		if comm.strip() != '':
			k_v = []
			k_v.append(int(table2.row(row)[5].value))
			k_v.append(comm)
			road_arr.append(k_v)	#每个元素	0：小区id,1：小区关键字

for item in road_arr:
	print(str(item[0]) + ',' + item[1] + ' ')