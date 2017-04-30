# coding:utf-8
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
f = codecs.open('4.txt','r','utf8') 
comm_arr = []
s = f.readlines() 
f.close() 
for line in s:  
	line = line.replace("\n","").encode('utf-8')
	l = line.split("\t")
	
	for j in range(2,6):
		if l[j].strip() != '':
			k_v = []
			k_v.append(l[0])
			k_v.append(l[j])
			comm_arr.append(k_v)

# for i in comm_arr:
# 	print(i[0] + ',' + i[1])


string = "东方巴黎"
getid = []
for i in comm_arr:
	# temp = []
	if len(i[1])<=len(string):
		start = string.find(i[1])		
	else:								#如果批量填id,不能这么用，只适合查询时给出提示
		start = i[1].find(string)

	if start >=0:
		temp = [start,i[1],i[0]]
		getid.append(temp)


for i in getid:
	print str(i[0]) +',' + i[1] +',' + i[2]