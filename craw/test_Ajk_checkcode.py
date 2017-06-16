#coding:utf-8
from spider import html_downloader,AJK_parser
import urllib2
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# downloader = html_downloader.HtmlDownloader()
# parser = AJK_parser.AjkParser()
url = 'http://xm.anjuke.com/sale/?from=navigation'
# url = 'http://xm.lianjia.com/ershoufang/'
req = urllib2.Request(url)
headers = {
    "Host":"xm.anjuke.com",
    # "Referer":"http://xm.anjuke.com/",
    }  
for key in headers:
    req.add_header(key,headers[key])
# agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
req.add_header("GET",url)
# req.add_header("User-Agent",agent)

try:
    response = urllib2.urlopen(req,timeout=10)
    html_cont = response.read()
    status = response.getcode()    
except urllib2.HTTPError,e:
    print e.code  
    print e.reason  
    print e.geturl()  
    print e.read()
    if e.code == 404:       #404找不到网页，是被禁了
        # raw_input("You have been forbidden,please stop the program now")
        print('aaaa')
# html_cont = downloader.download(url,False,True)
# print(html_cont)
# print(status)
# print(response.info())
# soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')
# title = soup.select('title')[0].get_text()
# print(title)








