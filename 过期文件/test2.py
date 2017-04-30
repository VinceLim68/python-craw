#coding:utf-8
from spider import html_downloader
from bs4 import BeautifulSoup
import re

# s='<span>2006年建造</span>'
# d1 = {'a':1,'b':2}
# d2 = {}
# d2['b'] = int(re.search('(\d{4})年', s).groups(0)[0])
# # print d2
# d1 = dict(d1, **d2) 
# print d1

s = '4房2厅2卫，162.00 平米，52962.96 元/平米，6/36层，南北，建筑年代：2005'.decode('utf-8')
d1 = {'a':1,'b':2}
d2 = {}
d2['b'] = int(re.search('年.*(\d{4})'.decode('utf-8'), s).groups(0)[0])
d1 = dict(d1, **d2) 
print d1