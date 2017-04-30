#coding:utf-8
from spider import html_downloader,AJK_parser
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def parse_floor(item):
    '''
    高层/(共30层)-->拆成楼层和总层数,        安居客、链家中使用
    传入：        item-->字符串        sep-->分隔符
    '''
    if '(' in unicode(item):
        sep = '('
    elif '/' in unicode(item):
        sep = '/'   
    elif '（' in unicode(item):
        sep = '（'   
    else:
        sep = '/'     
    try:

        total_floor = int(filter(str.isdigit,((item.split(sep)[1]) if sep in item else item).encode("utf-8")))
        index = item.split(sep)[0] if sep in item else " "  
        
        if unicode(index) == u" ":
            floor_index = 0
        elif u"高" in unicode(index):
            floor_index = int(total_floor*5/6)
        elif u"低" in unicode(index):
            floor_index = int(total_floor/6)
        else:
            floor_index = int(total_floor/2)
        # print(total_floor)
        # print(floor_index)
    except Exception, e:
        with open('logtest.txt','a+') as fout:
            fout.write('******' + str(datetime.datetime.now()) + ' *********Erro in parse_floor*************\n')
            fout.write('Parse Failt of :%s \n'%item.encode('utf8'))
            traceback.print_exc(file=fout) 
            print (traceback.format_exc())
    return floor_index,total_floor

def parse_item(string):
    # 2016.8.17增加：传入一个字符串，用正则判断它是面积？户型？单价？楼层？建成年份？优势？解析后返回一个键对值
    string = string.decode('utf8')
    parse_dict = {}

    r1_1 = '(\d+)平方米'.decode('utf8')
    r1_2 = '(\d+.?\d+)平米'.decode('utf8')        #厦门house的面积是浮点数
    r1_3 = '(\d+.?\d+)㎡'.decode('utf8')         #2016.9.13增加麦田的面积解析
    r2_1 = '\d+室'.decode('utf8')
    r2_2 = '\d+房'.decode('utf8')
    r3 = '(\d+)元/'.decode('utf8')
    r4 = '\d+层'.decode('utf8')
    r5_1 = '(\d{4})年'.decode('utf8')
    r5_2 = '年.*(\d{4})'.decode('utf8')


    if re.search(r1_1, string, flags=0):
        parse_dict['area'] = int(re.search(r1_1, string).groups(0)[0])
    elif re.search(r1_2, string, flags=0):
        parse_dict['area'] = int(round(float(re.search(r1_2, string).groups(0)[0]),0))
    elif re.search(r1_3, string, flags=0):                                          #2016.9.13增加麦田的面积解析
        parse_dict['area'] = int(round(float(re.search(r1_3, string).groups(0)[0]),0))
    elif re.search(r2_1, string, flags=0):
        parse_dict['spatial_arrangement'] = string.strip()
    elif re.search(r2_2, string, flags=0):
        parse_dict['spatial_arrangement'] = string.strip()
    elif re.search(r3, string, flags=0):
        pass        #单价准备自己计算，不取值
    elif re.search(r4, string, flags=0):
        parse_dict['floor_index'],parse_dict['total_floor'] = parse_floor(string)
    elif re.search(r5_1, string, flags=0):
        parse_dict['builded_year'] = int(re.search(r5_1, string).groups(0)[0])
    elif re.search(r5_2, string, flags=0):
        parse_dict['builded_year'] = int(re.search(r5_2, string).groups(0)[0])
    else:                           #re.search('[南北东西]', string, flags=0):
        parse_dict['advantage'] = string.strip()
    
    return parse_dict;





downloader = html_downloader.HtmlDownloader()
parser = AJK_parser.AjkParser()
# url = 'http://xm.ganji.com/fang5/o1/'
url = 'http://xm.anjuke.com/sale/p2/'
html_cont = downloader.download(url,False,True)
# print(html_cont)
# area_re = '(\d+.?\d+)万'.decode('utf8')
soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')
ischeck = soup.select("title")
print(ischeck[0].get_text()=="访问验证-安居客")
# parse_community = r"(.*)\s*\[(.*)-(.*)\s+(.+)\]"
# titles = soup.select("div.house-title > a")
# prices = soup.select('span.price-det')
# comms = soup.select('span.comm-address')
# houses = soup.select('div.house-details')
# # hxs = soup.select("span.js-huxing")
# # details = soup.select("p.list-word")
# # comms = soup.select("div.list-word")
# # prices = soup.select("em.sale-price")
# # areas = soup.select("span.js-area")
# i=1

# for title,price,comm,details in zip(titles,prices,comms,houses):
#     each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
#     print("********************************" + str(i))
#     i = i + 1
#     each_data['title'] = title.get('title')
#     each_data['details_url'] = title.get('href').split('?')[0] 
#     each_data['total_price'] = int(filter(str.isdigit,price.get_text().encode('utf8')))
#     each_data['community_name'],each_data['region'],each_data['block'],each_data['community_address'] = re.findall(parse_community,comm.get('title'))[0]
#     house = details.select('span')
#                 # 2016.8.17 重写了字段解析，抽象出一个parse_item方法
    # for h in house:
    #     # print(h)
    #     if len(h.attrs) == 0:
    #         # print(h)
    #         string = h.get_text().encode('utf8')
    #         print(string)
    #         d1 = {}
    #         d1 = parser.parse_item(string)
    #         print(d1)

    # print(house)
            # for key,value in d1.items():
            # # for key,value in each_data.items():
            #     print(key)
            #     print(value) 

# for hx,title,detail,comm,price,area in zip(hxs,titles,details,comms,prices,areas):
#     each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
#     each_data['title'] = title.get('title')
#     each_data['details_url'] = 'http://xm.ganji.com' + title.get('href')
#     for item in (detail.stripped_strings):
#         if item.strip() != '/' and item.strip() != '商品房' and '更新' not in item.strip() :
#             d1 = {}
#             d1 = parse_item(item.strip())
#             if d1.has_key('advantage') and each_data.has_key('advantage'):
#                 d1['advantage'] = each_data['advantage'] + ',' + d1['advantage'] 
#             each_data = dict(each_data, **d1) 
#     each_data['community_name'] = comm.stripped_strings.next().strip()
#     each_data['total_price'] = int(round(float(price.get_text()),0))
#     each_data['area'] = float(re.search('(\d+.?\d+)㎡'.decode('utf8'),area.get_text()).groups(0)[0])
#     each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
#     each_data['from'] = "ganji"

#     print(str(i)+'*'*50)
#     i+=1

# pagelinks = soup.select("ul.pageLink > li > a")

# for link in pagelinks:
#     if link.has_attr('href'):print("http://xm.ganji.com" + link['href'])





