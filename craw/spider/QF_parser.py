#coding:utf-8
from html_parser import HtmlParser
import urllib2  
from bs4 import BeautifulSoup
import  re

class QfParser(HtmlParser):
    """docstring for QfParser"""
    
    def confir(self,str):
        for i in range(0,32):
            str = str.replace(chr(i),'')
        return  str

    def showinfo(self,item):
        item = str(item)
        if len(item)%2 == 0 :
            print (item)        
        else:
            print (item) + ' '
        return

    def _get_new_datas(self,soup):
        
        page_datas = []
        # page_comms = []

        titles = soup.select("h3 > a.showKeyword")
        listitems = soup.select("div.listings-item-characteristics.clearfix ")
        remainders = soup.select("p.remainder-info")
        prices = soup.select("p.listings-item-price > span")
        addrs = soup.select("div.listings-item-address")

        for title,listitem,remainder,price,addr in zip(titles,listitems,remainders,prices,addrs):
            each_data = {}

            each_data['title'] = title.get_text()
            each_data['details_url'] = "http://xiamen.qfang.com" + title.get('href')
            
            for item in list(listitem.stripped_strings):
                item = self.confir(item)
                each_data['builded_year'] = 0
                if u"建" in unicode(item):
                    each_data['builded_year'] = int(filter(str.isdigit,item.encode("utf-8")))
                elif u"层" in unicode(item):
                    each_data['floor_index'],each_data['total_floor'] = self.parse_floor(unicode(item))      #2016.5.28用标准化来解析楼层和层次

                else:
                    each_data['advantage'] = item


            each_data['spatial_arrangement'] = list(remainder.stripped_strings)[0]
            each_data['area'] = int(float(re.findall(self.r1,list(remainder.stripped_strings)[1])[0][0]))

            each_data['total_price'] = int(price.get_text())

            # each_data['community_name'] = self.confir(list(addr.stripped_strings)[0]).strip()
            # block = list(addr.stripped_strings)[2].split('\r\n')
            # each_data['region'] = self.confir(block[0])
            # each_data['block'] = self.confir(block[1])
            
            block = list(addr.stripped_strings)
            each_data['community_name'] = block[0].strip()            
            
            each_data['region'] = block[2].strip()
            each_data['block'] = block[3].strip()
            if len(block) >= 6 : each_data['community_address'] = block[5].strip()

            each_data['price'] = float(each_data['total_price']*10000/each_data['area']) 
            each_data['from'] = "Qfang"

            each_data = self.pipe(each_data)        #2016.6.4增加一个专门的数据处理
            if each_data:
                page_datas.append(each_data)

            # if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
            #     page_datas.append(each_data)
        #         page_comms.append(each_data['community_name'])
        # return page_datas,page_comms
        return page_datas

        

    def _get_new_urls(self , soup):

        new_urls = set()
        links = soup.select("p.turnpage_num > a")

        if len(links) == 0 :
            print "Only 1 page!!"
        else:
            for link in links:
                if link.get('href') != None:
                    new_urls.add("http://xiamen.qfang.com%s" %link.get('href'))
        return new_urls
