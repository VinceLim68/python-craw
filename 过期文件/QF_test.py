#coding:utf-8
from bs4 import BeautifulSoup
import urllib2
from spider import mytools,html_parser
import re 
import datetime
import traceback
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
r1 = re.compile(r"(\d+\.?\d*)(.*)")

# url = 'http://xm.anjuke.com/sale/p1/'
url = 'http://xiamen.qfang.com/sale/f3'
# print url
response = urllib2.urlopen(url).read()
# print response
soup = BeautifulSoup(response,'html.parser',from_encoding='urf-8')
parse = html_parser.HtmlParser()

titles = soup.select("h3 > a.showKeyword")
listitems = soup.select("div.listings-item-characteristics.clearfix ")
remainders = soup.select("p.remainder-info")
prices = soup.select("p.listings-item-price > span")
addrs = soup.select("div.listings-item-address")

for title,listitem,remainder,price,addr in zip(titles,listitems,remainders,prices,addrs):
    block = list(addr.stripped_strings)
    print len(block)
    print block[0]
    print block[2]
    print block[3]
    print block[5]
    # for item in addr.stripped_strings:
    #     print j,item
    #     j += 1
    # print addr
    print '*'*25
    # each_data = {}

    # each_data['title'] = title.get_text()
    # each_data['details_url'] = "http://xiamen.qfang.com" + title.get('href')
    
    # for item in list(listitem.stripped_strings):
    #     item = mytools.confir(item)
    #     each_data['builded_year'] = 0
    #     if u"建" in unicode(item):
    #         each_data['builded_year'] = int(filter(str.isdigit,item.encode("utf-8")))
    #     elif u"层" in unicode(item):
    #         each_data['floor_index'],each_data['total_floor'] = self.parse_floor(unicode(item))      #2016.5.28用标准化来解析楼层和层次
    #     else:
    #         each_data['advantage'] = item


    # each_data['spatial_arrangement'] = list(remainder.stripped_strings)[0]
    # each_data['area'] = int(float(re.findall(r1,list(remainder.stripped_strings)[1])[0][0]))

    # each_data['total_price'] = int(price.get_text())

    # each_data['community_name'] = mytools.confir(list(addr.stripped_strings)[0]).strip()
    # block = list(addr.stripped_strings)[2].split('\r\n')
    # each_data['region'] = mytools.confir(block[0])
    # each_data['block'] = mytools.confir(block[1])

    # each_data['price'] = float(each_data['total_price']*10000/each_data['area']) 
    # each_data['from'] = "Qfang"
    # for key,value in each_data.items():mytools.pri( " %s : %s"%(key,value))

    
