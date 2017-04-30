#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from __future__ import print_function
from html_parser import HtmlParser
from bs4 import BeautifulSoup
import datetime
import mytools
import re
import traceback  

class AjkParser(HtmlParser):

    def _get_new_urls(self , soup):
        new_urls = set()
        multi_page = soup.find('div',class_='multi-page')
        if multi_page == None :
            print("Only 1 page!!")
        else:
            links = multi_page.find_all('a')
            for url in links:
                new_urls.add(url['href'])
        return new_urls
           


    def _get_new_datas(self,soup):

        page_datas = []

        titles = soup.select("div.house-title > a")
        houses = soup.select('div.house-details')
        comms = soup.select('span.comm-address')
        prices = soup.select('span.price-det')
        parse_community = r"(.*)\s*\[(.*)-(.*)\s+(.+)\]"

        for title,details,comm,price in zip(titles,houses,comms,prices):
            #2016.6.1安居客抓取时内存溢出，重新用select写解析
            # 2016.8.16 下面几个设初始值
            each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
            # each_data['title'] = href.get_text().strip().encode('utf8')                                              
            each_data['title'] = title.get('title')
            # each_data['details_url'] = title.get('href')
            each_data['details_url'] = title.get('href').split('?')[0]      #2016.12.19 url字段太长，取?之前
            
   
            try:                    #2016.8.1 这里解析也时有出差，把它保留下来
                each_data['total_price'] = int(filter(str.isdigit,price.get_text().encode('utf8')))
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('AJK解析total_price出错，待解析的数据：' + price.get_text() )
                    traceback.print_exc(file=fout) 
                    print(traceback.format_exc())
            
            try:
                each_data['community_name'],each_data['region'],each_data['block'],each_data['community_address'] = re.findall(parse_community,comm.get('title'))[0]
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('Parse Failt of :%s \n'%comm.get('title'))
                    traceback.print_exc(file=fout) 
                    print (traceback.format_exc())
            each_data['community_name'] = each_data['community_name'].strip()
            
            try:
                house = details.select('span')
                # 2016.8.17 重写了字段解析，抽象出一个parse_item方法
                for h in house:
                    if len(h.attrs) == 0:
                        string = h.get_text().encode('utf8')
                        d1 = {}
                        d1 = self.parse_item(string)
                        each_data = dict(each_data, **d1) 
                each_data['price'] = round(each_data['total_price']*10000/each_data['area'],0)
                each_data['from'] = "AJK" 
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('      待解析的数据：\n' )
                    for i1 in house:
                        fout.write(str(i1) + '\n')
                    fout.write('\n      字段数：' + str(len(house)) +'\n' )
                    traceback.print_exc(file=fout) 
                    print(traceback.format_exc())

            each_data = self.pipe(each_data)        #2016.6.4增加一个专门的数据处理

            if each_data:
                page_datas.append(each_data)


        return page_datas           #2016.5.30直接从字典里提取数据，不再另外加一个小区名的list





