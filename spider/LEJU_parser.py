#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from __future__ import print_function
from html_parser import HtmlParser
from bs4 import BeautifulSoup
import datetime
import mytools
import re
import traceback  

class LejuParser(HtmlParser):

    def _get_new_urls(self , soup):
        new_urls = set()
        pagelinks = soup.select("div.page > a")
        if pagelinks == None :
            print("Only 1 page!!")
        else:
            for link in pagelinks:
                if link.has_attr('href'):new_urls.add(link['href'])
        return new_urls
           

    def _get_new_datas(self,soup):

        page_datas = []

        details = soup.select("div.house-info")
        comms = soup.select("div.house-info > a ")
        positions = soup.select("div.house-position")
        prices = soup.select("span.georgia")
        titles = soup.select("h3 > a")

        for title,comm,detail,position,price in zip(titles,comms,details,positions,prices):

            each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
            each_data['title'] = title.get('title')
            each_data['details_url'] = title.get('href')
            mr20 = detail.select("span.mr20")
            posi = position.select("span")
            for j in range(1,len(posi)):
                out = {}
                out = self.parse_item(posi[j].get_text())
                if len(out) > 0:
                    if each_data.has_key('advantage') and out.has_key('advantage'):
                        each_data['advantage'] = each_data['advantage'] + ',' + out['advantage']        
                    else:
                        each_data = dict(each_data, **out) 
            for item in mr20:
                d1 = {}
                d1 = self.parse_item(item.get_text())
                if len(d1) > 0:
                    if each_data.has_key('advantage') and d1.has_key('advantage'):
                        each_data['advantage'] = each_data['advantage'] + ',' + d1['advantage']
                    else:
                        each_data = dict(each_data, **d1) 

            each_data['community_name'] = comm.get_text()
            each_data['total_price'] = int(round(float(price.get_text()),0))
            each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
            each_data['from'] = "lejv"

            each_data = self.pipe(each_data)        #2016.6.4增加一个专门的数据处理

            if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
                page_datas.append(each_data)
            else:
                if mytools.ShowInvalideData(each_data):page_datas.append(each_data)

        return page_datas 


