#coding:utf-8
from spider import html_downloader,AJK_parser
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


downloader = html_downloader.HtmlDownloader()
parser = AJK_parser.AjkParser()
# url = 'http://xm.ganji.com/fang5/o1/'
url = 'http://xm.anjuke.com/sale/p2/'
html_cont = downloader.download(url,False,True)
print(html_cont)
soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')

# titles = soup.select("dl.f-list-item-wrap > dd > a")
# items = soup.select('dd.dd-item.size')
# comms = soup.select('span.area')
# prices = soup.select('div.price')

# i=1

# for title,item,comm,price in zip(titles,items,comms,prices):
# # for title,price,comm,details in zip(titles,prices,comms,houses):
#     each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
#     print("********************************" + str(i))
#     each_data['title'] = title.get('title')
#     each_data['details_url'] = 'http://xm.ganji.com' + title.get('href')
#     # print(item)
#     house = item.select('span')
#     for h in house:
#         d1 = {}
#         d1 = parser.parse_item(h.get_text().encode('utf8'))
#         each_data = dict(each_data, **d1) 
#     each_data['total_price'] = int(round(float(price.stripped_strings.next()),0))
#     each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
#     each_data['from'] = "ganji"     
#     # print(each_data['total_price'])
#     # print(price)

#     each_data['community_name'] = comm.stripped_strings.next().split(' ')[0].replace('.','').encode('utf8')

#     i = i + 1

#     for key,value in each_data.items():
#         print(key)
#         print(value) 







