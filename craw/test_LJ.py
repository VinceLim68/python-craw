#coding:utf-8
from spider import html_downloader,html_parser
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


downloader = html_downloader.HtmlDownloader()
url = 'http://xm.lianjia.com/ershoufang/pg1/'
html_cont = downloader.download(url,False,True)
parser = html_parser.HtmlParser()
soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')

titles = soup.select("div.title > a")
houseinfo = soup.select("div.houseInfo")
positionInfo = soup.select("div.positionInfo")
totalprices = soup.select("div.totalPrice")
i = 1

for title,info,position,totalPrice in zip(titles,houseinfo,positionInfo,totalprices):
    
    print(str(i)+'*'*50) 
    i = i + 1

    each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
    each_data['title'] = title.get_text()
    each_data['details_url'] = title.get('href')
    each_data['total_price'] = int(round(float(re.search('(\d+.?\d+)万'.decode('utf8'),totalPrice.get_text()).groups(0)[0]),0))

    info_item = (info.get_text().split('|'))



    each_data['community_name'] = info_item[0].strip()      # 第1个总是小区名称
    for i in range(1,len(info_item)):
        # print(info_item[i].strip())
        d1 = {}
        d1 = parser.parse_item(info_item[i].strip())
        if d1.has_key('advantage') and each_data.has_key('advantage'):
            d1['advantage'] = each_data['advantage'] + ',' + d1['advantage'] 
        each_data = dict(each_data, **d1) 

    position = position.get_text().replace('\t','').replace('\n','').split()
    each_data['block'] = position[-1]
    for item in position[0].split(')'):
        d1 = {}
        d1 = parser.parse_item(item.strip())
        each_data = dict(each_data, **d1)

    each_data['price'] = float(each_data['total_price']*10000/each_data['area'])
    each_data['from'] = "lianjia"


    for key,value in each_data.items():
        print("%20s:   %s" %(key,value) )
    

# pagelinks = soup.select("ul.pageLink > li > a")

# for link in pagelinks:
#     if link.has_attr('href'):print("http://xm.ganji.com" + link['href'])




