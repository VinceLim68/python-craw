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
url = 'http://xm.anjuke.com/sale/p3/'
html_cont = downloader.download(url,False,True)

# soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')
soup = BeautifulSoup(html_cont,'lxml',from_encoding='urf-8')
# ischeck = soup.select("title")
# print(ischeck[0].get_text()=="访问验证-安居客")
# parse_community = r"(.*)\s*\[(.*)-(.*)\s+(.+)\]"
# parse_community = r"(.*?)&nbsp;&nbsp(.*?)"

titles = soup.select("div.house-title > a")
prices = soup.select('span.price-det')
comms = soup.select('span.comm-address')
houses = soup.select('div.house-details')

i=1

for title,price,comm,details in zip(titles,prices,comms,houses):
    each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
    print("********************************" + str(i))
    i = i + 1
    each_data['title'] = title.get('title')
    each_data['details_url'] = title.get('href').split('?')[0] 
    each_data['total_price'] = int(filter(str.isdigit,price.get_text().encode('utf8')))
    comminfo = comm.get('title').split()
    # dd = cc
    # for ite in dd:
    #     print(ite)
    # each_data['community_name'],each_data['region'],each_data['block'],each_data['community_address'] = re.findall(parse_community,comm.get('title'))[0]
    # print(re.findall(parse_community,comm.get('title')))
    # print(cc.split[0])
    each_data['community_name'] = comminfo[0]
    each_data['region'],each_data['block'],each_data['community_address'] = comminfo[1].split('-',2)
    # print(dd[0])
    # for i2 in dd[1].split('-',2):
    #     print i2
    house = details.select('span')
                # 2016.8.17 重写了字段解析，抽象出一个parse_item方法
    for h in house:
        if len(h.attrs) == 0:
            # print(h)
            string = h.get_text().encode('utf8')
            # print(string)
            d1 = {}
            d1 = parser.parse_item(string)
            # print(d1)
            if d1.has_key('advantage') and each_data.has_key('advantage'):
                d1['advantage'] = each_data['advantage'] + ',' + d1['advantage'] 
            each_data = dict(each_data, **d1) 

    for key,value in each_data.items():
        print('%20s : %s' %(key,value))

# for hx,title,detail,comm,price,area in zip(hxs,titles,details,comms,prices,areas):
#     each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
#     each_data['title'] = title.get('title')
#     each_data['details_url'] = 'http://xm.ganji.com' + title.get('href')
#     for item in (detail.stripped_strings):
#         if item.strip() != '/' and item.strip() != '商品房' and '更新' not in item.strip() :
#             d1 = {}
#             d1 = parse_item(item.strip())
#             if d1.has_key('advantage') and each_data.has_key('advantage'):
#                 d1['advantage'] = each_data['advantage'] + ',' + d1['advantage'] 
#             each_data = dict(each_data, **d1) 
#     each_data['community_name'] = comm.stripped_strings.next().strip()
#     each_data['total_price'] = int(round(float(price.get_text()),0))
#     each_data['area'] = float(re.search('(\d+.?\d+)㎡'.decode('utf8'),area.get_text()).groups(0)[0])
#     each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
#     each_data['from'] = "ganji"

#     print(str(i)+'*'*50)
#     i+=1

# pagelinks = soup.select("ul.pageLink > li > a")

# for link in pagelinks:
#     if link.has_attr('href'):print("http://xm.ganji.com" + link['href'])