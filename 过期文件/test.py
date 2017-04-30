#coding:utf-8
from spider import html_downloader
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

price = int(round(float(re.search('(\d+.?\d+)万','369.45万').groups(0)[0]),0))
print(price)