#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from html_parser import HtmlParser
from bs4 import BeautifulSoup
import mytools
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re

class SfParser(HtmlParser):

    def parse(self,html_cont,fromwhere):
        #搜房网用lxml解析有问题，来不及分析，先用回html.parser
        if html_cont is None or html_cont == False:
            print('This is nothing in the scraw content')
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')        
        new_urls = self._get_new_urls(soup)
        new_datas = self._get_new_datas(soup)
        return new_urls,new_datas

    def _get_new_urls(self , soup):
        new_urls = set()
        links = soup.select("div.fanye > a")
        if links == None :
            print "Only 1 page!!"
        else:
            for link in links:
                if link.get('href') != None:
                    new_urls.add("http://esf.xm.fang.com" + link.get('href'))
        return new_urls
           


    def _get_new_datas(self,soup):

        page_datas = []
        # page_comms = []
        
        titles = soup.select("p.title > a")
        houses = soup.select("dd.info > p.mt12")
        comms = soup.select("p.mt10 > a > span")
        areas = soup.select("div.area.alignR ")
        prices = soup.select("span.price")

        for title,house,comm,area,price in zip(titles,houses,comms,areas,prices):
            each_data = {}

            each_data['title'] = title.get_text()
            each_data['details_url'] = "http://esf.xm.fang.com" + title.get('href')
            each_data['advantage'] = "None"
            each_data['builded_year'] = 0
            each_data['floor_index'] = 0
            for item in list(house.stripped_strings):
                if u"向" in unicode(item):
                    each_data['advantage'] = item
                elif u"建" in unicode(item):
                    each_data['builded_year'] = int(filter(str.isdigit,item.encode("utf-8")))
                elif u"室" in unicode(item):
                    each_data['spatial_arrangement'] = item
                elif u"层" in unicode(item):
                    each_data['floor_index'],each_data['total_floor'] = self.parse_floor(unicode(item))
                    # if '(' in unicode(item):
                    #     each_data['floor_index'],each_data['total_floor'] = self.parse_floor(unicode(item),'(')
                    # else:
                    #     each_data['floor_index'],each_data['total_floor'] = self.parse_floor(unicode(item),'/')
                    # each_data['floor_index'] = int(item.split("/")[0]) if "/" in item else 0           #层次
                    # each_data['total_floor'] = int(filter(str.isdigit,((item.split("/")[1]) if "/" in item else item).encode("utf-8")))

            each_data['community_name'] = comm.get_text().strip()
            each_data['area'] = int(filter(str.isdigit,list(area.stripped_strings)[0].encode("utf-8")))
            each_data['total_price'] = int(float(price.get_text()))
            each_data['price'] = round(float(each_data['total_price'])*10000/each_data['area'],0)
            each_data['from'] = "Soufan"
            
            #舍弃没有关键字段的信息
            # if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
            #     page_datas.append(each_data)
            # else:
            #     if mytools.ShowInvalideData(each_data):page_datas.append(each_data)
            each_data = self.pipe(each_data)        #2016.6.4增加一个专门的数据处理
            if each_data:
                page_datas.append(each_data)

        return page_datas





