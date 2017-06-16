#coding:utf-8
from spider import html_downloader,GJ_parser
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


downloader = html_downloader.HtmlDownloader()
url = 'http://xm.esf.leju.com/house/'
html_cont = downloader.download(url,False,True)
parser = GJ_parser.GjParser()
soup = BeautifulSoup(html_cont,'lxml',from_encoding='urf-8')


details = soup.select("div.house-info")
comms = soup.select("div.house-info > a ")
positions = soup.select("div.house-position")
prices = soup.select("span.georgia")
titles = soup.select("h3 > a")
i=1

for title,comm,detail,position,price in zip(titles,comms,details,positions,prices):

    each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
    each_data['title'] = title.get('title')
    each_data['details_url'] = title.get('href')
    mr20 = detail.select("span.mr20")
    posi = position.select("span")
    for j in range(1,len(posi)):
        out = {}
        out = parser.parse_item(posi[j].get_text())
        if len(out) > 0:
            if each_data.has_key('advantage') and out.has_key('advantage'):
                each_data['advantage'] = each_data['advantage'] + ',' + out['advantage']        
            else:
                each_data = dict(each_data, **out) 
    for item in mr20:
        d1 = {}
        d1 = parser.parse_item(item.get_text())
        if len(d1) > 0:
            if each_data.has_key('advantage') and d1.has_key('advantage'):
                each_data['advantage'] = each_data['advantage'] + ',' + d1['advantage']
            else:
                each_data = dict(each_data, **d1) 

    each_data['community_name'] = comm.get_text()
    each_data['total_price'] = int(round(float(price.get_text()),0))
    each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
    each_data['from'] = "lejv"
    for key,value in each_data.items():
        print("%s----->%s" %(key,value) )
    print(str(i)+'*'*50)
    i+=1

pagelinks = soup.select("div.page > a")

for link in pagelinks:
    if link.has_attr('href'):print(link['href'])




