#coding:utf-8
from spider import html_downloader,GJ_parser
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


downloader = html_downloader.HtmlDownloader()
url = 'http://xm.ganji.com/fang5/o1/'
html_cont = downloader.download(url,False,True)
parser = GJ_parser.GjParser()
soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')


details = soup.select("dd.dd-item.size")
comms = soup.select("dd.dd-item.address > span ")
prices = soup.select("span.num.js-price")
titles = soup.select("dd.dd-item.title > a")
i=1

for title,detail,comm,price in zip(titles,details,comms,prices):

    each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
    each_data['title'] = title.get('title')
    each_data['details_url'] = 'http://xm.ganji.com' + title.get('href')
    for item in (detail.stripped_strings):
        d1 = {}
        d1 = parser.parse_item(item)
        each_data = dict(each_data, **d1) 
    each_data['community_name'] = comm.stripped_strings.next().strip()
    each_data['total_price'] = int(round(float(price.get_text()),0))
    each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
    each_data['from'] = "ganji"
    for key,value in each_data.items():
        print("%s----->%s" %(key,value) )
    print(str(i)+'*'*50)
    i+=1

# pagelinks = soup.select("ul.pageLink > li > a")

# for link in pagelinks:
#     if link.has_attr('href'):print("http://xm.ganji.com" + link['href'])




