#coding:utf-8
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
#import urlparse

#这里原来有传入page_url，是为了在_get_new_urls中补齐链接格式，现在不太必要
class HtmlParser(object):

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")

    def _get_new_urls_fromAJK(self , soup):
        # <div class="multi-page">
        #     <i class="iPre">上一页</i> 
        #     <i class="curr">1</i>
        #     <a href="http://xm.anjuke.com/sale/p2-rd1/?kw=%E7%A6%8F%E6%BB%A1%E5%B1%B1%E5%BA%84#filtersort">2</a>
        #     <a href="http://xm.anjuke.com/sale/p3-rd1/?kw=%E7%A6%8F%E6%BB%A1%E5%B1%B1%E5%BA%84#filtersort">3</a>
        #     <a href="http://xm.anjuke.com/sale/p4-rd1/?kw=%E7%A6%8F%E6%BB%A1%E5%B1%B1%E5%BA%84#filtersort">4</a>
        #     <a href="http://xm.anjuke.com/sale/p5-rd1/?kw=%E7%A6%8F%E6%BB%A1%E5%B1%B1%E5%BA%84#filtersort">5</a>
        #     <a href="http://xm.anjuke.com/sale/p6-rd1/?kw=%E7%A6%8F%E6%BB%A1%E5%B1%B1%E5%BA%84#filtersort">6</a>
        #     <a href="http://xm.anjuke.com/sale/p7-rd1/?kw=%E7%A6%8F%E6%BB%A1%E5%B1%B1%E5%BA%84#filtersort">7</a>
        #     <i class="aDotted">...</i>
        #     <a href="http://xm.anjuke.com/sale/p2-rd1/?kw=%E7%A6%8F%E6%BB%A1%E5%B1%B1%E5%BA%84#filtersort" class="aNxt">下一页 &gt;</a>
        # </div>
        new_urls = set()
        multi_page = soup.find('div',class_='multi-page')
        if multi_page == None :
            print "Only 1 page!!"
        else:
            links = multi_page.find_all('a')
            for url in links:
                new_urls.add(url['href'])
        return new_urls

    def _get_new_urls_fromXMHOUSE(self,soup):
        new_urls = set()
        multi_page = soup.find('div',class_='pageBlue fr')
        if multi_page == None :
            print "Only 1 page!!"
        else:
            links = multi_page.find_all('a')
            for url in links:
                if url.has_attr('href'):
                    new_urls.add('http://esf.xmhouse.com' + url['href'])
        return new_urls
               


    def _get_new_datas_fromAJK(self,soup):

        # <div class="house-details">      #每个house_detail是一个挂牌信息
        #     <div class="house-title">       #"house-titel"给出是一个挂牌信息里面的摘要内容
        #         <a data-from=""  title="年底急卖  水晶森林 楼王位置 业主豪华自住装修 读实验二小" 
        #         href="http://xm.anjuke.com/prop/view/A424599117?from=comm_one&spread=commsearch_p" target='_blank' class="">
        #             年底急卖  
        #             <em class="em_kw" >
        #                 <em class="em_kw" >水</em>
        #                 <em class="em_kw" >晶</em>
        #                 <em class="em_kw" >森</em>
        #                 <em class="em_kw" >林</em>
        #             </em>
        #             楼王位置 业主豪华自住装修 读实验二小
        #         </a>
        #         <i class="icon-dt">多图</i>            
        #     </div>
        #     <div>                           #这里给出了一些细节
        #         <span>257平方米</span>
        #         <em>|</em>
        #         <span>3室2厅</span>
        #         <em>|</em>
        #         <span>31128元/m²</span>
        #         <em>|</em>
        #         <span>10/13层</span>
        #         <em>|</em>
        #         <span>2009年建造</span>
        #         <em>|</em>
        #         <span>BRT沿</span>            
        #     </div>
        #     <div>                           #这里给出了地址
        #         <span class="comm-address" title="水晶森林&nbsp;&nbsp;[湖里-枋湖 双十中学枋湖新校区正南面]">
        #             <em class="em_kw" >
        #                 <em class="em_kw" >水</em>
        #                 <em class="em_kw" >晶</em>
        #                 <em class="em_kw" >森</em>
        #                 <em class="em_kw" >林</em>
        #             </em>
        #             &nbsp;&nbsp;[湖里-枋湖&nbsp;双十中学枋湖新校区正南面]                
        #         </span>
        #     </div>
        #     <div class="details-bottom">
        #         <span class="broker-name">陈顺琴</span>
        #     </div>
        # </div>
        # #这个下面给出了一个总价
        # <div class="pro-price">
        #     <span class="price-det">
        #         <strong>800</strong>
        #         万</br>
        #     </span>
        #     <div class="fcj">
        #     </div>
        # </div>   

        page_datas = []
        
        # 正则：把面积、单价中的数字与后面的单位分开
        r = re.compile(r'(\d+\.?\d*)(\D*)')     
                
        #找出所有的挂牌信息  
        house_detail = soup.find_all(class_="house-details")

        for x in range(0,len(house_detail)):

            each_data = {}

            #每个挂牌信息的“摘要内容”
            each_data['title'] = house_detail[x].find_all("a")[0]['title']

            # 取出挂牌信息里的细节内容。放在<span>标签里的数据，一般有7-8个
            # 前6个分别代表面积、户型、单价、楼层（第几层/共几层的格式）、建成年份、优势
            # 但是第六个“优势”可能会不存在
            details = house_detail[x].find_all("span")
            each_data['area'] = int(re.findall(r,details[0].string)[0][0])                  #面积
            each_data['area_unit'] = re.findall(r,details[0].string)[0][1]                  #面积单位
            each_data['spatial_arrangement'] = details[1].string                            #空间布局
            each_data['price'] = int(re.findall(r"\d+\.?\d*",details[2].string)[0])         #单价
            if "/" in details[3].string:
                each_data['floor_index'] = int(details[3].string.split("/")[0])             #层次
                each_data['total_floor'] = details[3].string.split("/")[1]                  #总楼层
            else:
                each_data['floor_index'] = int("0")                                         #没有层次，可能是别墅
                each_data['total_floor'] = details[3].string
            each_data['builded_year'] = details[4].string                                   #建成年份
            if len(details) < 8:                                                            #优势：如果没有，补None
                each_data['advantage'] = "None"
            else:
                each_data['advantage'] = details[5].string

                     
            #总价信息是house_detail的兄弟标签        
            price = house_detail[x].find_next_siblings("div")
            #取出总价，它在price下的<span>下
            #第一个子节点是回车，第二个是<strong>，它的文本内容是总价，第三个子节点是价格单位
            each_data['total_price'] = int(price[0].span.contents[1].string)
            each_data['total_price_unit'] = price[0].span.contents[2]
            
            #链接地址
            each_data['details_url'] = house_detail[x].find_all("a")[0]['href']

            #找到小区的名称和地址
            community = house_detail[x].find_all(class_="comm-address")[0]['title']
            parse_community = r"(.*)\s*\[(.*)-(.*)\s+(.+)\]"
            try:
                each_data['community_name'],each_data['region'],each_data['block'],each_data['community_address'] = re.findall(parse_community,community)[0]
            except:
                print "Parse failed" + community

            page_datas.append(each_data)
        return page_datas

    def _get_new_datas_fromXMHOUSE(self,soup):
        houses = soup.find_all(class_="detail")

        r1 = re.compile(r"(\d+\.?\d*)(.*)")             #正则：数字+单位
        r2 = re.compile(r"(\d+).*")                     #正则：取字符串中的数字

        page_datas = []
        #num = 0

        for i in range(0,len(houses)):
            house = houses[i]
            each_data = {}

            each_data['title'] = house.find("a")['title']                                           #标题
            each_data['details_url'] = "http://esf.xmhouse.com" + house.find("a")['href']           #网址链接
            each_data['community_name'] = house.find(class_="xuzhentian").find("a").string          #小区名称

            #物业信息在一个长字段里，用“，”分开
            house_info = re.search(r'<span style="margin-left: 5px; color: #000000">.*</span>(.*) <div',str(house),
                re.S).group(1).replace('<br/>','').replace('\r\n','').replace(' ','').split('，')
            each_data['spatial_arrangement'] = house_info[0].strip()                                #户型
            each_data['area'],each_data['area_unit'] = re.findall(r1,house_info[1])[0]              #面积及单位
            each_data['price'],each_data['price_unit'] = re.findall(r1,house_info[2])[0]            #单价及单位
            if "/" in house_info[3]:
                each_data['floor_index'] = int(house_info[3].split("/")[0])                         #层次
                each_data['total_floor'] = int(re.findall(r2,house_info[3].split("/")[1])[0])       #总楼层
            else:
                each_data['floor_index'] = int("0")                                                 #没有层次，可能是别墅
                each_data['total_floor'] = int(re.findall(r2,house_info[3])[0])
            each_data['towards'] = house_info[4]                                                    #朝向
            each_data['builded_year'] =  int(re.findall(r2,house_info[5])[0])                       #建成年份


            house2 = str(house.find_next_siblings("dd"))                                            #总价在兄弟tag中
            h4,h5 = re.findall(r'<em>(.*)</em><font style="color: #f30">(.*)</font>',house2)[0]     #取出总价和单位
            each_data['total_price'] = int(re.findall(r2,h4)[0])                                    #有些奇怪的字符串要处理掉
            each_data['total_price_unit'] = h5.decode("unicode-escape").replace('\r\n','').strip('')

            page_datas.append(each_data)
        return page_datas

    def parse(self,html_cont,fromwhere):

        if html_cont is None:
            print('This is nothing in the scraw content')
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')
        if fromwhere == 1:
            new_urls = self._get_new_urls_fromAJK(soup)
            new_datas = self._get_new_datas_fromAJK(soup)
        if fromwhere == 2:
            new_urls = self._get_new_urls_fromXMHOUSE(soup)
            new_datas = self._get_new_datas_fromXMHOUSE(soup)

        return new_urls,new_datas


