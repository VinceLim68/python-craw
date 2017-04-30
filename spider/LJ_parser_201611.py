#coding:utf-8
from html_parser import HtmlParser
import mytools
import urllib2 
from bs4 import BeautifulSoup
import re

class LjParser(HtmlParser):

    def _get_new_datas(self,soup):       
		page_datas = []
		# page_comms = []

		titles = soup.select("h2 > a")
		wheres = soup.select("div.where")
		cons = soup.select("div.con")
		prices = soup.select("div.price > span.num")
		
		for title,where,con,price in zip(titles,wheres,cons,prices):
			each_data = {}
			each_data['title'] = title.get_text()
			each_data['details_url'] = title.get('href')
			each_data['community_name'],each_data['spatial_arrangement'],each_data['area'],each_data['advantage'] = list(where.stripped_strings)
			each_data['community_name'] = each_data['community_name'].strip()
			each_data['area'] = int(float(re.findall(self.r1,each_data['area'])[0][0]))
			each_data['builded_year'] = 0

			for item in con.strings:				#2016.6.3 con.strings返回 NavigableString 字符串. 通过 unicode() 方法可以直接将 NavigableString 对象转换成Unicode字符串
				if u"年" in unicode(item):			#原来的方法有很多无效数据
					each_data['builded_year'] = int(filter(str.isdigit,item.encode("utf-8")))
				if u"层" in unicode(item):
					each_data['floor_index'],each_data['total_floor'] = self.parse_floor(unicode(item))      #2016.5.28用标准化来解析楼层和层次                  

			each_data['total_price'] = int(price.get_text())
			each_data['price'] = float(each_data['total_price']*10000/each_data['area']) 
			each_data['from'] = "lianjia"

			if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
				page_datas.append(each_data)
			else:
				if mytools.ShowInvalideData(each_data):page_datas.append(each_data)
		return page_datas


    def _get_new_urls(self , soup):

		new_urls = set()
		# links = soup.select("div.page-box")
		links = soup.select("div.house-lst-page-box")		#2016.11.11修改，网页改了
		
		if len(links) == 0 :
			print "Only 1 page!!"
		else:
			t_page = eval(links[0].get('page-data'))['totalPage']
			url = links[0].get('page-url')
			for i in range(1,t_page+1):
				new_urls.add("http://xm.lianjia.com" + url.replace("{page}",str(i)))
		return new_urls



