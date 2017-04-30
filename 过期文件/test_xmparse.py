#coding:utf-8
from bs4 import BeautifulSoup
import urllib2
import re

def confir(str):
    for i in range(0,32):
        str = str.replace(chr(i),'')
    str = str.replace(' ','')
    return  str

def pri(string):
    if len(string) % 2 != 0:
        string = string + ' '
    print string

url = 'http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html?mustupdate=now'

data = urllib2.urlopen(url).read()
soup = BeautifulSoup(data,'html.parser',from_encoding='urf-8')
i = 1
details = soup.select('dd.detail ')
hrefs = soup.select('span.c_blue0041d9.aVisited.f14B > a')
comms = soup.select('span.xuzhentian > a')
prices = soup.select('span > em')

for detail,href,comm,price in zip(details,hrefs,comms,prices):

	each_data = {}
	# print comm.next_sibling

	each_data['title'] = href.get_text().strip().encode('utf8')
	each_data['community_name'] = comm.get_text().strip().encode('utf8')
	each_data['details_url'] = "http://esf.xmhouse.com" + href.get('href')
	each_data['total_price'] = int(price.get_text())
	h_infos = re.search(r'<span style="margin-left: 5px; color: #000000">.*</span>(.*) <div',str(detail),re.S)\
			.group(1).replace('<br/>','').replace('\r\n','').replace(' ','').split('，')

	for item in h_infos:
		if '层' in item:
			each_data['floor_index'] = int(item.split("/")[0]) if "/" in item else 0                         #层次
			# print each_data['floor_index']
			each_data['total_floor'] = int(filter(str.isdigit,item.split("/")[1] if "/" in item else item) )   #总楼层
			# print each_data['total_floor'] 
		if '年' in item:
			each_data['builded_year'] = int(filter(str.isdigit,item))
			# print each_data['builded_year']
		if '房' in item:
			each_data['spatial_arrangement'] = item.strip()
			# pri(each_data['spatial_arrangement'])
		if '南' in item or '北' in item or '东' in item or '西' in item:
			each_data['advantage'] = item
			# pri(each_data['advantage'])
		if '平' in item and '元' not in item:
			each_data['area'] = round(float(item.split('平')[0]),0)				
			# print each_data['area']
	
	each_data['price'] = round(each_data['total_price']*10000/each_data['area'],0)
	each_data['from'] = "XMHouse"                                                               #数据来源
	for (d,x) in each_data.items():
 		print d + "----->" + str(x)
	print  str(i) + '*'*25
	i += 1