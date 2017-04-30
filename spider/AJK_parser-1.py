#coding:utf-8
#做成一个继承的类，只是增加_get_new_urls()和_get_new_datas()
from __future__ import print_function
from html_parser import HtmlParser
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import traceback  

class AjkParser(HtmlParser):

    def _get_new_urls(self , soup):
        new_urls = set()
        multi_page = soup.find('div',class_='multi-page')
        if multi_page == None :
            print("Only 1 page!!")
        else:
            links = multi_page.find_all('a')
            for url in links:
                new_urls.add(url['href'])
        return new_urls
           


    def _get_new_datas(self,soup):

        page_datas = []
        
        houses = soup.find_all(class_="house-details")

        for house in houses:

            each_data = {}

            try:

                #每个挂牌信息的“摘要内容”
                each_data['title'] = house.find_all("a")[0]['title']

                # 取出挂牌信息里的细节内容。放在<span>标签里的数据，一般有7-8个
                # 前6个分别代表面积、户型、单价、楼层（第几层/共几层的格式）、建成年份、优势
                # 但是第六个“优势”可能会不存在
                details = house.find_all("span")
                each_data['area'] = int(re.findall(self.r1,details[0].string)[0][0])                  #面积
                each_data['area_unit'] = re.findall(self.r1,details[0].string)[0][1]                  #面积单位
                each_data['spatial_arrangement'] = details[1].string                            #空间布局
                # each_data['floor_index'] = int(details[3].string.split("/")[0]) if "/" in details[3].string else 0           #层次
                # each_data['total_floor'] = int(re.findall(self.r2,details[3].string.split("/")[1])[0]) if "/" in details[3].string else int(re.findall(self.r2,details[3].string)[0])                 #总楼层
                
                each_data['floor_index'],each_data['total_floor'] = self.parse_floor(details[3].string,'(')
                each_data['builded_year'] = 0 if len(details) < 7 else int(re.findall(self.r2,details[4].string)[0])                               #建成年份
                #优势：如果没有，补None
                each_data['advantage'] = "None" if len(details) < 8 else details[5].string

                    
                #总价信息是house_detail的兄弟标签        
                price = house.find_next_siblings("div")
                #取出总价，它在price下的<span>下
                #第一个子节点是回车，第二个是<strong>，它的文本内容是总价，第三个子节点是价格单位
                each_data['total_price'] = int(price[0].span.contents[1].string)
                each_data['total_price_unit'] = price[0].span.contents[2]
                
                each_data['price'] = int(each_data['total_price'])*10000/each_data['area']           #直接计算单价，不采用采集的数据
                #链接地址
                each_data['details_url'] = house.find_all("a")[0]['href']

                #找到小区的名称和地址
                community = house.find_all(class_="comm-address")[0]['title']
                parse_community = r"(.*)\s*\[(.*)-(.*)\s+(.+)\]"
                try:
                    each_data['community_name'],each_data['region'],each_data['block'],each_data['community_address'] = re.findall(parse_community,community)[0]
                except:
                    print("Parse failed %s"%community)
                    traceback.print_exc(file=open('log.txt','a+')) 
                    traceback.print_exc()

                each_data['community_name'] = each_data['community_name'].strip()
                each_data['from'] = "AJK" 
            except:
                for key,value in each_data.items():print( " %s : %s"%(key,value))
            if each_data.has_key('total_floor') and each_data.has_key('total_price') and each_data.has_key('area') and each_data.has_key('community_name'):
                page_datas.append(each_data)
                # page_comms.append(each_data['community_name'])
        # return page_datas,page_comms
        return page_datas           #2016.5.30直接从字典里提取数据，不再另外加一个小区名的list





