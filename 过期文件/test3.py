#coding:utf-8
from spider import html_downloader
from bs4 import BeautifulSoup
import re
import sys


def parse_floor(item):
    '''
    高层/(共30层)-->拆成楼层和总层数,        安居客、链家中使用
    传入：        item-->字符串        sep-->分隔符
    '''
    if '(' in unicode(item):
        sep = '('
    elif '/' in unicode(item):
        sep = '/'   
    else:
        sep = '/'     
    try:

        total_floor = int(filter(str.isdigit,((item.split(sep)[1]) if sep in item else item).encode("utf-8")))
        index = item.split(sep)[0] if sep in item else " "  
        if unicode(index) == u" ":
            floor_index = 0
        elif u"高" in unicode(index):
            floor_index = int(total_floor*5/6)
        elif u"低" in unicode(index):
            floor_index = int(total_floor/6)
        else:
            floor_index = int(total_floor/2)
    except Exception, e:
        with open('logtest.txt','a+') as fout:
            fout.write('******' + str(datetime.datetime.now()) + ' *********Erro in parse_floor*************\n')
            fout.write('Parse Failt of :%s \n'%item.encode('utf8'))
            traceback.print_exc(file=fout) 
            print (traceback.format_exc())
    return floor_index,total_floor

def parse_item(string):
	string = string.decode('utf8')
	parse_dict = {}

	r1_1 = '(\d+)平方米'.decode('utf8')
	r1_2 = '(\d+.?\d+)平米'.decode('utf8')
	r2_1 = '\d+室'.decode('utf8')
	r2_2 = '\d+房'.decode('utf8')
	r3 = '(\d+)元/'.decode('utf8')
	r4 = '\d+层'.decode('utf8')
	r5_1 = '(\d{4})年'.decode('utf8')
	r5_2 = '年.*(\d{4})'.decode('utf8')


	if re.search(r1_1, string, flags=0):
	    parse_dict['area'] = int(re.search(r1_1, string).groups(0)[0])
	elif re.search(r1_2, string, flags=0):
	    parse_dict['area'] = int(float(re.search(r1_2, string).groups(0)[0]))
	elif re.search(r2_1, string, flags=0):
	    parse_dict['spatial_arrangement'] = string.strip()
	elif re.search(r2_2, string, flags=0):
	    parse_dict['spatial_arrangement'] = string.strip()
	elif re.search(r3, string, flags=0):
	    pass        #单价准备自己计算，不取值
	elif re.search(r4, string, flags=0):
	    parse_dict['floor_index'],parse_dict['total_floor'] = parse_floor(string)
	elif re.search(r5_1, string, flags=0):
	    parse_dict['builded_year'] = int(re.search(r5_1, string).groups(0)[0])
	elif re.search(r5_2, string, flags=0):
	    parse_dict['builded_year'] = int(re.search(r5_2, string).groups(0)[0])
	else:                           #re.search('[南北东西]', string, flags=0):
	    parse_dict['advantage'] = string.strip()

	return parse_dict;

reload(sys)
sys.setdefaultencoding("utf-8")	
downloader = html_downloader.HtmlDownloader()
url = 'http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s0_itp_b0_it_if_ih_p-_ar-_pt_o0_ps20_2.html?mustupdate=now'
html_cont = downloader.download(url,False,True)
soup = BeautifulSoup(html_cont,'lxml',from_encoding='urf-8')
# print (soup)
houses = soup.select('dd.detail')
i = 1
for details in houses:
	h_infos = re.search(r'<span style="margin-left: 5px; color: #000000">.*</span>(.*) <div',str(details),re.S)\
		.group(1).replace('<br/>','').replace('\r\n','').replace(' ','').split('，')

	each_data = {}
	for item in h_infos :
		
		d1 = {}
		d1 = parse_item(item)
		each_data = dict(each_data, **d1)



	for key,value in each_data.items():
		print(key,value)
	# print(t[2])
	# h_infos = t[3].replace('<br/>','').replace('\r\n','').replace(' ','').split('，')
	# # j=0
	# for item1 in h_infos:		
	# 	print(item1)
		# d1 = {}
  #       d1 = parse_item(i1)
  #       print(d1)
  #       each_data = dict(each_data, **d1) 

# for item in each_data:
# 	print(item)	
		# print(str(j)+"-"*40)
		# j += 1

	# print(str(details).encode('utf8'))
	# house = details.select('span')
	# # source = "东西南北".decode('utf8')   
	# # temp = source 
	# # p1 =re.compile(source)
	# # print(type(house))
	# for h in house:
	# 	if len(h.attrs) == 0:
	# 		string = h.get_text().encode('utf8')
	# 		# print(string)
	# 		print(parse_item(string))
	print(str(i)+"*"*50)
	i += 1



# new_urls = set()
# multi_page = soup.find('div',class_='pageBlue fr')
# print(multi_page)
# if multi_page == None :
#     print "Only 1 page!!"
# else:
#     links = multi_page.find_all('a')
#     for url in links:
#         if url.has_attr('href'):
#             new_urls.add('http://esf.xmhouse.com' + url<a href="/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_1.html"><span>1</span></a>['href'])/html/body/div[9]/div[2]/div/div[4]/ul/li[2]/div
# print(new_urls)
# body > div.warp.martop > div.l_sider.fl > div > div.page.c_black555 > ul > li:nth-child(2) > div
# records = soup.select("table.tab4 > tr")
# lands = []

# for record in records:
# 	# print('8'*50)
# 	data = {}
# 	r2 = record.select('td')
# 	data['landNo'] = (r2[0].contents[0].get('title').encode("utf-8"))
# 	data['href'] = (r2[0].contents[0].get('href'))
# 	data['use'] = (r2[1].contents[1].get('title').encode("utf-8"))
# 	data['address'] = (r2[2].contents[0].get('title').encode("utf-8"))
# 	data['date'] = (r2[3].get('title').encode("utf-8"))
# 	data['acreage'] = (r2[4].get('title').encode("utf-8"))
# 	data['floorArea'] = (r2[5].get('title').encode("utf-8"))
# 	data['price'] = (r2[6].get_text().encode("utf-8"))
# 	data['user'] = (r2[7].get('title').encode("utf-8"))

# 	lands.append(data)

# for i in lands:
# 	for key,value in i.items():
# 		print(key,value)


