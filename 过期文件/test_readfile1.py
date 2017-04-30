# coding:utf-8
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
f = codecs.open('5.txt','r','utf8') 
comm_arr = []
s = f.readlines() 
f.close() 
for line in s:  
	line = line.replace("\n","").encode('utf-8')
	l = line.split("\t")
	
	for j in range(2,6):			#这个循环是，如果小区名有别名，把它们分拆成不同的元素加入字典
		if l[j].strip() != '':
			k_v = []
			k_v.append(l[0])
			k_v.append(l[j])
			comm_arr.append(k_v)	#每个元素	0：小区id,1：小区关键字



string = "东方巴黎宝龙中心划片莲花二村实领秀中山验二小、一中双十 三房,临近植物园,私家花园"
# print(len("http://www.cnblogs.com/way_testlife/archive/2010/06/14/1758276.html"))
# string2 = "公安局宿舍/阳台山/一中/万寿"
# string2 = "公安局宿舍"

# print(len(comm_arr))
getid = []
for i in comm_arr:
	# temp = []
	# print(i)
	key_words = i[1].split("/")		#对带“/”的关键字进行拆分，第一个是关键字，后面是补充区分的
	# print(key_words)
	start = string.find(key_words[0])
	if start >= 0:
		lenth=len(key_words)
		if lenth > 1:
			for j in range(1,lenth):
				if string.find(key_words[j]) >=0:
					temp = [start,i[1],i[0]]
					getid.append(temp)
					break
		else:
			temp = [start,i[1],i[0]]
			getid.append(temp)




			# print(comm_arr[i])


	# if len(i[1])<=len(string):
	# 	start = string.find(i[1])		
	# else:								#如果批量填id,不能这么用，只适合查询时给出提示
	# 	start = i[1].find(string)
# print(len(getid))
		
getid.sort(key=lambda x:x[0]) 
first = getid[0]
for l in range(1,len(getid)):
	if(getid[l][0] > first[0]):
		break
	else:
		if len(getid[l][1]) > len(first[1]):
			first = getid[l]
		# print str(getid[l][0]) +',' + getid[l][1] +',' + getid[l][2]

print str(first[0]) + ',' + first[1] + first[2]


# for i in getid:
# 	print str(i[0]) +',' + i[1] +',' + i[2]