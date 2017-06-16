#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from __future__ import print_function
from html_parser import HtmlParser
from bs4 import BeautifulSoup
import datetime
import mytools
import re
import traceback  

class MTParser(HtmlParser):

    def _get_new_urls(self , soup):
        new_urls = set()
        links = soup.select("#paging > a")
     
        if links == None :
            print("Only 1 page!!")
        else:
            for link in links:
                if link.get('href') != None:
                    new_urls.add('http://xm.maitian.cn' + link.get('href'))
        return new_urls
           


    def _get_new_datas(self,soup):

        page_datas = []

        titles = soup.select("h1 > a")
        infos = soup.select("p.house_info")
        hots = soup.select("p.house_hot")
        areas = soup.select("div.the_area span")
        prices = soup.select("div.the_price span")
        splitby = re.compile(r']|,|\s')

        for title,info,hot,area,price in zip(titles,infos,hots,areas,prices):

            each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
                                          
            each_data['title'] = title.get_text().encode('utf8')
            each_data['details_url'] = 'http://xm.maitian.cn' + title.get('href')
            
   
            try:                    
                each_data['total_price'] = int(filter(str.isdigit,price.get_text().encode('utf8')))
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('麦田解析total_price出错，待解析的数据：' + price.get_text() )
                    traceback.print_exc(file=fout) 
                    print(traceback.format_exc())
            
            try:
                each_data['community_name'] = splitby.split(info.get_text().encode('utf8'))[-1].strip()
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('Parse Failt of :%s \n'%info.get_text())
                    traceback.print_exc(file=fout) 
                    print (traceback.format_exc())
            
            try:
                #麦田的格式，这里是户型、优势和楼层
                temp = mytools.clearStr(hot.text.encode('utf8')).split('|')
                for item in temp:
                    d1 = {}
                    d1 = self.parse_item(item)
                    each_data = dict(each_data, **d1)
                
                #这是解析面积
                each_data = dict(each_data, **self.parse_item(area.get_text().encode('utf8')))

                each_data['price'] = round(each_data['total_price']*10000/each_data['area'],0)
                each_data['from'] = "MT" 
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('      待解析的数据：\n' )
                    for i1 in house:
                        fout.write(str(i1) + '\n')
                    fout.write('\n      字段数：' + str(len(house)) +'\n' )
                    traceback.print_exc(file=fout) 
                    print(traceback.format_exc())

            each_data = self.pipe(each_data)        

            if each_data:
                page_datas.append(each_data)


        return page_datas          





