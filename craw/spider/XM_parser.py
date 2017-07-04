#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from html_parser import HtmlParser
import mytools
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import datetime
import traceback

class XmParser(HtmlParser):

    # def parse(self,html_cont,fromwhere):

    #     #厦门网用lxml解析有问题，来不及分析，先用回html.parser
    #     if html_cont is None or html_cont == False:
    #         print('This is nothing in the scraw content')
    #         return
    #     soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')
 
    #     new_urls = self._get_new_urls(soup)
    #     new_datas = self._get_new_datas(soup)
    #     return new_urls,new_datas


    def _get_new_urls(self,soup):
        new_urls = set()

        # 2016.8.15重写了url解析
        urls = soup.select(".pageBlue > a")
        if len(urls):
            for url in urls:
                if url.has_attr('href'):
                    new_urls.add('http://esf.xmhouse.com' + url['href'])
        else:
            print "There is only 1 page!!"
        # multi_page = soup.find('div',class_='pageBlue fr')
        # if multi_page == None :
        #     print "Only 1 page!!"
        # else:
        #     links = multi_page.find_all('a')
        #     for url in links:
        #         if url.has_attr('href'):
        #             new_urls.add('http://esf.xmhouse.com' + url['href'])
        return new_urls

    def _get_new_datas(self,soup):
        page_datas = []
        # page_comms = []
        details = soup.select('dd.detail ')
        hrefs = soup.select('span.c_blue0041d9.aVisited.f14B > a')
        comms = soup.select('span.xuzhentian > a')
        prices = soup.select('span > em')

        for detail,href,comm,price in zip(details,hrefs,comms,prices):

            # each_data = {'advantage':'','builded_year':0,'spatial_arrangement':''}
            each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
            each_data['title'] = href.get_text().strip().encode('utf8')
            each_data['community_name'] = comm.get_text().strip().encode('utf8')
            each_data['details_url'] = "http://esf.xmhouse.com" + href.get('href')
            each_data['total_price'] = int(price.get_text())
            h_infos = re.search(r'<span style="margin-left: 5px; color: #000000">.*</span>(.*) <div',str(detail),re.S)\
                    .group(1).replace('<br/>','').replace('\r\n','').replace(' ','').split('，')

            for item in h_infos:
                try:
                    #2016.8.22使用新的专门解析函数
                    d1 = {}
                    d1 = self.parse_item(item)
                    each_data = dict(each_data, **d1)
                    

                except Exception, e:
                    with open('logtest.txt','a+') as fout:
                        fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                        fout.write('      获取的数据：' )
                        for i1 in h_infos:
                            fout.write(i1 + ',')
                        fout.write('\n      XmParser解析时发生错误的Item是： ' + str(item) + '\n')
                        traceback.print_exc(file=fout) 
                        print traceback.format_exc()
                       
            each_data['from'] = "XMHouse" 
            each_data = self.pipe(each_data) 
            if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
                each_data['price'] = round(each_data['total_price']*10000/each_data['area'],0)
                page_datas.append(each_data)
            else:                
                if mytools.ShowInvalideData(each_data):page_datas.append(each_data)

        return page_datas