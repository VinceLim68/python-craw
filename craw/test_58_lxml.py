#coding:utf-8
from spider import html_downloader,AJK_parser,mytools
# from bs4 import BeautifulSoup
from lxml import etree
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

downloader = html_downloader.HtmlDownloader()
parser = AJK_parser.AjkParser()
url = 'http://xm.58.com/ershoufang/pn1/'
html_cont = downloader.download(url,False,True)

# 使用lxml解析
sel = etree.HTML(html_cont.encode('utf-8'))                 

# 解析页码
pages = sel.xpath('//div[@class="pager"]/a/@href')
# for page in pages:
#     print(page)
# soup = BeautifulSoup(html_cont,'lxml',from_encoding='utf-8')

titles = sel.xpath('//h2[@class="title"]/a')
prices = sel.xpath('//p[@class="sum"]/b')
houses = sel.xpath('//div[@class="list-info"]')


i=1

for title,price,house in zip(titles,prices,houses):
    each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
    print("********************************" + str(i))
    i = i + 1
    each_data['title'] = title.text
    each_data['details_url'] = title.get('href')
    each_data['total_price'] = int(filter(str.isdigit,price.text.encode('utf8')))
    # print(house.text)
    # print(house.tostring(html))

    details = house.xpath('./p')
    # for detail in details:
        # print(detail.text)
    spans = details[0].xpath('./span')
    for span in spans:
        string = span.text
        if string is not None:
            string = mytools.clearStr(span.text).encode('utf8')
            d1 = {}
            d1 = parser.parse_item(string)
            each_data = dict(each_data, **d1) 
    
    comms = details[1].xpath('.//a')
    # print( details[1].xpath('string(.)'))
    each_data['community_name'] = comms[0].text
    
    if comms[0].get('href') is None:
        each_data['comm_url'] = ''
    else:
        each_data['comm_url'] = 'http://xm.58.com' + comms[0].get('href')
    each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
    each_data['from'] = "58"
    for key,value in each_data.items():
        print('%20s : %s' %(key,value))




# pagelinks = soup.select("ul.pageLink > li > a")

# for link in pages:
    # if link.has_attr('href'):print("http://xm.ganji.com" + link['href'])
    # print(link.get('href'))