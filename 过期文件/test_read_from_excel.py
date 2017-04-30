# coding:utf-8
import xlrd
data = xlrd.open_workbook('comm.xlsx')
table = data.sheet_by_name(u'Sheet3')
nrows = table.nrows
ncols = table.ncols
# print(ncols)
# for i in range(nrows):
# 	print table.row_values(i)
# print(nrows)
comm_arr = []
i=0
for row in range(1,nrows):
	for col in range(7,ncols):			#这个循环是，如果小区名有别名，把它们分拆成不同的元素加入字典
		comm = table.row(row)[col].value.encode("utf8")
		if comm.strip() != '':
			# print(int(table.row(row)[5].value))
			k_v = []
			k_v.append(int(table.row(row)[5].value))
			k_v.append(comm)
			comm_arr.append(k_v)	#每个元素	0：小区id,1：小区关键字
	# 		print(comm+" ")
	# print(str(i) + "-"*20)
	# i += 1

for item in comm_arr:
	print(str(item[0]) + ',' + item[1]+" ")