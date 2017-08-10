#coding:utf-8
from html_parser import HtmlParser
import mytools
import urllib2 
from bs4 import BeautifulSoup
import re

class LjParser(HtmlParser):

    # 这些是2016.11.17重写的，原来那个出现了解析错误
    
    def _get_new_datas(self,soup):       
        page_datas = []

        titles = soup.select("div.title > a")
        houseinfo = soup.select("div.houseInfo")
        positionInfo = soup.select("div.positionInfo")
        totalprices = soup.select("div.totalPrice")
        for title,info,position,totalPrice in zip(titles,houseinfo,positionInfo,totalprices):
            # each_data有些需要设置初始值
            each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
            each_data['title'] = title.get_text()
            each_data['details_url'] = title.get('href')
            each_data['total_price'] = int(round(float(re.search('(\d+.?\d+)万'.decode('utf8'),totalPrice.get_text()).groups(0)[0]),0))

            info_item = (info.get_text().split('|'))

            each_data['community_name'] = info_item[0].strip()      # 第1个总是小区名称
            for i in range(1,len(info_item)):
                d1 = {}
                d1 = self.parse_item(info_item[i].strip())
                if d1.has_key('advantage') and each_data.has_key('advantage'):
                    d1['advantage'] = each_data['advantage'] + ',' + d1['advantage'] 
                each_data = dict(each_data, **d1) 

            position = position.get_text().replace('\t','').replace('\n','').split()
            each_data['block'] = position[-1]

            if ')' not in position[0]:              #链前的别墅会用'4层2008年建'的形式，加入')'，以便分隔
                position[0] = position[0].replace('层', '层)')

            for item in position[0].split(')'):     #2017.4.1链家格式有改
                d1 = {}
                # d1 = self.parse_item(position[i].strip())
                d1 = self.parse_item(item.strip())          #2017.4.1链家格式有改
                each_data = dict(each_data, **d1)

            each_data['price'] = float(each_data['total_price']*10000/each_data['area'])
            each_data['from'] = "lianjia"

            if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
                page_datas.append(each_data)
            else:
                if mytools.ShowInvalideData(each_data):page_datas.append(each_data)
        
        return page_datas


    def _get_new_urls(self , soup):

        new_urls = set()
        # links = soup.select("div.page-box")
        links = soup.select("div.house-lst-page-box")       #2016.11.11修改，网页改了
        
        if len(links) == 0 :
            print "Only 1 page!!"
        else:
            t_page = eval(links[0].get('page-data'))['totalPage']
            url = links[0].get('page-url')
            for i in range(1,t_page+1):
                new_urls.add("http://xm.lianjia.com" + url.replace("{page}",str(i)))
        return new_urls

    def _ischeck(self,soup):
        # 判断是否是验证界面
        ischeck = soup.select("title")
        if len(ischeck) > 0:            #如果找不到title,就认为不是验证界面
            iscode = ischeck[0].get_text().strip() == "验证异常流量-链家网"
        else:
            iscode = False
        return iscode


