#coding:utf-8
from html_parser import HtmlParser
import mytools
import urllib2 
from bs4 import BeautifulSoup
import re

class GjParser(HtmlParser):

	def parse(self,html_cont,fromwhere):

		if html_cont is None or html_cont == False:
			print('This is nothing in the scraw content')
			return
		soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')   #2016.12.1赶集网要用html.parser解析才行
		new_urls = self._get_new_urls(soup)
		new_datas = self._get_new_datas(soup)
		return new_urls,new_datas

	def _get_new_datas(self,soup):       
		page_datas = []
		# 赶集网2017.03改版

		details = soup.select("dd.dd-item.size")
		comms = soup.select("dd.dd-item.address > span ")
		prices = soup.select("span.num.js-price")
		titles = soup.select("dd.dd-item.title > a")


		for title,detail,comm,price in zip(titles,details,comms,prices):

			each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
			each_data['title'] = title.get('title')
			each_data['details_url'] = 'http://xm.ganji.com' + title.get('href')
			for item in (detail.stripped_strings):
				d1 = {}
				d1 = self.parse_item(item)
				each_data = dict(each_data, **d1) 
			each_data['community_name'] = comm.stripped_strings.next().strip().split(' ')[0].replace('.','').encode('utf8')
			each_data['total_price'] = int(round(float(price.get_text()),0))
			each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
			each_data['from'] = "ganji"
			each_data = self.pipe(each_data)

			if each_data:
			# if each_data and each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
				page_datas.append(each_data)
			else:
				if mytools.ShowInvalideData(each_data):page_datas.append(each_data)
		
		return page_datas


	def _get_new_urls(self , soup):

		new_urls = set()
		links = soup.select("ul.pageLink > li > a")

		if len(links) == 0 :
			print "Only 1 page!!"
		else:
			for link in links:
				if link.has_attr('href'):
					new_urls.add("http://xm.ganji.com" + link['href'])			

		return new_urls



