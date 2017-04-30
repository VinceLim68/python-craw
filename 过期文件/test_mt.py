#coding:utf-8
from bs4 import BeautifulSoup
from spider import html_downloader,mytools,html_parser		# import HtmlParser
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")
splitby = re.compile(r']|,|\s')

downloader = html_downloader.HtmlDownloader()
parser = html_parser.HtmlParser()

url = "http://xm.maitian.cn/esfall/PG3"
content = downloader.download(url,False,True)
soup = BeautifulSoup(content,'lxml',from_encoding='urf-8')

titles = soup.select("h1 > a")
infos = soup.select("p.house_info")
hots = soup.select("p.house_hot")
areas = soup.select("div.the_area span")
prices = soup.select("div.the_price span")

# links = soup.select("#paging > a")

# for link in links:
# 	if link.get('href') != None:
# 		print('http://xm.maitian.cn' + link.get('href')) 


for title,info,hot,area,price in zip(titles,infos,hots,areas,prices):
	#取出标题
	mytools.pri(title.get_text().encode('utf8'))
	
	#取出链接
	print('http://xm.maitian.cn' + title.get('href'))
	
	#以下取出小区名
	info_item = info.get_text().encode('utf8')
	# print(info_item)
	print(splitby.split(info_item)[-1])

	# for item in splitby.split(info_item):
	# 	print(item)
	temp = mytools.clearStr(hot.text.encode('utf8')).split('|')
	# print(temp)
	for item in temp:
		print(item)
		print(parser.parse_item(item))

	#取出面积
	print(area.get_text().encode('utf8'))
	print(parser.parse_item(area.get_text().encode('utf8')))

	#取出总价
	print(price.get_text().encode('utf8'))

	print("-"*40)
