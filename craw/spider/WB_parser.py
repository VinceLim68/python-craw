#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from __future__ import print_function
from html_parser import HtmlParser
# from bs4 import BeautifulSoup
from lxml import etree
import datetime
import mytools
import re
import traceback  

class WBParser(HtmlParser):

    def parse(self,html_cont,fromwhere):
        # 重写解析主模块，使用lxml
        sel = etree.HTML(html_cont.encode('utf-8'))   
        
        #辨识是否有验证码的代码
        if self._ischeck(sel):
            new_urls = raw_input('checkcode!!!  checkcode!!!  \ncheckcode!!!  checkcode!!!\nPlease input how many seconds you want to delay:')
            new_datas = 'checkcode'
        else:
            new_urls = self._get_new_urls(sel)      #解析页码
            new_datas = self._get_new_datas(sel)    #解析数据
        return new_urls,new_datas

    def _get_new_urls(self , sel):
        new_urls = set()
        pages = sel.xpath('//div[@class="pager"]/a/@href')
        if pages == None :
            print("Only 1 page!!")
        else:
            for url in pages:
                new_urls.add(url)
        return new_urls


    def _get_new_datas(self,sel):

        page_datas = []

        titles = sel.xpath('//h2[@class="title"]/a')
        prices = sel.xpath('//p[@class="sum"]/b')
        houses = sel.xpath('//div[@class="list-info"]')

        for title,price,house in zip(titles,prices,houses):
            each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
            each_data['title'] = title.text
            each_data['details_url'] = title.get('href')
            each_data['total_price'] = int(filter(str.isdigit,price.text.encode('utf8')))

            details = house.xpath('./p')
            spans = details[0].xpath('./span')
            for span in spans:
                string = span.text
                if string is not None:
                    string = mytools.clearStr(string).encode('utf8')
                    d1 = {}
                    d1 = self.parse_item(string)
                    each_data = dict(each_data, **d1) 
            
            comms = details[1].xpath('.//a')
            each_data['community_name'] = comms[0].text
            
            if comms[0].get('href') is None:
                each_data['comm_url'] = ''
            else:
                each_data['comm_url'] = 'http://xm.58.com' + comms[0].get('href')
            each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
            each_data['from'] = "58"

            each_data = self.pipe(each_data)       

            if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
                page_datas.append(each_data)
            else:
                if mytools.ShowInvalideData(each_data):page_datas.append(each_data)
                

        return page_datas           





