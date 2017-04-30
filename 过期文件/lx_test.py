#coding:utf-8
from spider import url_manager,html_downloader,AJK_parser,html_outputer,SF_parser,QF_parser,LJ_parser,XM_parser,mytools
import urllib2
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

r1 = re.compile(r"(\d+\.?\d*)(.*)")
url = 'http://xm.lianjia.com/ershoufang/pg1/'
response = urllib2.urlopen(url).read()
parse = LJ_parser.LjParser()
# print response
soup = BeautifulSoup(response,'html.parser',from_encoding='urf-8')

titles = soup.select("h2 > a")
wheres = soup.select("div.where")
cons = soup.select("div.con")
prices = soup.select("div.price > span.num")
i = 0
for title,where,con,price in zip(titles,wheres,cons,prices):
	each_data = {}
	i += 1

	each_data['title'] = title.get_text()
	each_data['details_url'] = title.get('href')
	each_data['community_name'],each_data['spatial_arrangement'],each_data['area'],each_data['advantage'] = list(where.stripped_strings)
	each_data['community_name'] = each_data['community_name'].strip()
	each_data['area'] = int(float(re.findall(r1,each_data['area'])[0][0]))
	each_data['builded_year'] = 0

	print "*"*25 + str(i)
	for item in con.strings:
		if u"年" in unicode(item):
			each_data['builded_year'] = int(filter(str.isdigit,item.encode("utf-8")))
		if u"层" in unicode(item):
			each_data['floor_index'],each_data['total_floor'] = parse.parse_floor(item,'(')      #2016.5.28用标准化来解析楼层和层次                  

	each_data['total_price'] = int(price.get_text())
	each_data['price'] = float(each_data['total_price']*10000/each_data['area']) 
	each_data['from'] = "lianjia"
	if each_data.has_key('total_floor'):
		for key,value in each_data.items():mytools.pri(" %s : %s"%(key,value))
	else:
		print "++"*20

