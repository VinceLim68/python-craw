#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from __future__ import print_function
from html_parser import HtmlParser
from bs4 import BeautifulSoup
# from lxml import etree
from lxml import html
import datetime
import mytools
import re
import traceback  

class WBParser(HtmlParser):

    def parseB(self,html_cont):
        # 58同城主页面的数据格式与每个小区下的页面格式不相同，小区页面用 parseB()来抓取
        sel = BeautifulSoup(html_cont,'lxml',from_encoding='urf-8')
        if self._ischeck(sel):
            new_urls = raw_input('checkcode!!!  checkcode!!!  \ncheckcode!!!  checkcode!!!\nPlease input how many seconds you want to delay:')
            new_datas = 'checkcode'
        else:
            new_urls = self._get_new_urls_B(sel)      #解析页码
            new_datas = self._get_new_datas_B(sel)    #解析数据
        return new_urls,new_datas
    
    def _get_new_urls_B(self , sel):
        new_urls = set()
        pages = sel.select("div.pagerNumber > a")
        if pages == None :
            print("Only 1 page!!")
        else:
            for url in pages:
                new_urls.add(url.get('href'))
        return new_urls

    def _get_new_datas_B(self,sel):

        page_datas = []

        houses = sel.select('td.t')
        titles = sel.select('td.t > a.t')
        prices = sel.select('td.tc > b.pri')
        spans = sel.select('td.tc')

        for span,house,title,price in zip(spans,houses,titles,prices):
            each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
            each_data['title'] = title.get_text()
            each_data['details_url'] = title.get('href')
            
            each_data['total_price'] = int(filter(str.isdigit,price.get_text().encode('utf8')))

            # 解析面积
            item = span.select('span.f14')
            d1 = self.parse_item(item[1].get_text())
            each_data = dict(each_data, **d1) 

            comm = house.select('.a_xq1')
            each_data['community_name'] = comm[1].get_text()

            hss = house.select('span.c_ccc')

            for hs in hss:
                string = hs.next_sibling
                if string is not None:
                    string = mytools.clearStr(string).encode('utf8')
                    d1 = {}
                    d1 = self.parse_item(string)
                    if d1.has_key('advantage') and each_data.has_key('advantage'):
                        each_data['advantage'] = each_data['advantage'] + '/' + d1['advantage']
                    else:
                        each_data = dict(each_data, **d1) 
             
            each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
            each_data['from'] = "58"

            each_data = self.pipe(each_data)       

            if each_data:
            # if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
                page_datas.append(each_data)
            else:
                if mytools.ShowInvalideData(each_data):page_datas.append(each_data)
                
        return page_datas    

    def parse(self,html_cont,fromwhere):
        # 重写解析主模块，使用lxml
        # sel = etree.HTML(html_cont.encode('utf-8'))   
        sel = html.fromstring(html_cont.encode('utf-8'))
        
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

            if each_data:
            # if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
                page_datas.append(each_data)
            else:
                if mytools.ShowInvalideData(each_data):page_datas.append(each_data)
                

        return page_datas           





