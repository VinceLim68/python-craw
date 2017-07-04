#coding:utf-8
from spider import html_downloader,AJK_parser,mytools
from bs4 import BeautifulSoup
# from lxml import etree
# from lxml import html
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

downloader = html_downloader.HtmlDownloader()
parser = AJK_parser.AjkParser()
url = 'http://xm.58.com/xiaoqu/lunenglingxiucheng1/ershoufang/pn_154/'
html_cont = downloader.download(url,False,True)
with open('html.txt','w+') as fout:      
    fout.write(html_cont)
                
# 使用lxml解析
# sel = etree.HTML(html_cont.encode('utf-8'))                 
# sel = html.fromstring(html_cont.encode('utf-8'))
sel = BeautifulSoup(html_cont,'lxml',from_encoding='urf-8')

# sel = html.parse(url)
# 解析页码
# pages = sel.xpath('//div[@class="pagerNumber"]/a/@href')
pages = sel.select("div.pagerNumber > a")
for page in pages:
    print(page.get('href'))

# titles = sel.xpath('//td[@class="t"]/a[@class="t"]')
# prices = sel.xpath('//td[@class="tc"]/b[@class="pri"]')
houses = sel.select('td.t')
titles = sel.select('td.t > a.t')
prices = sel.select('td.tc > b.pri')
spans = sel.select('td.tc')
# print(type(titles))

i=1
# print(len(prices))
# print(len(titles))
# for title in titles:
for span,house,title,price in zip(spans,houses,titles,prices):
    each_data = {'builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}

    print("*****************************************************" + str(i))
    i = i + 1

    each_data['title'] = title.get_text()
    each_data['details_url'] = title.get('href')
    
    each_data['total_price'] = int(filter(str.isdigit,price.get_text().encode('utf8')))

    # 解析面积
    item = span.select('span.f14')
    d1 = parser.parse_item(item[1].get_text())
    each_data = dict(each_data, **d1) 

    comm = house.select('.a_xq1')
    each_data['community_name'] = comm[1].get_text()


    hss = house.select('span.c_ccc')

    for hs in hss:
        string = hs.next_sibling
        if string is not None:
            string = mytools.clearStr(string).encode('utf8')
            d1 = {}
            d1 = parser.parse_item(string)
            if d1.has_key('advantage') and each_data.has_key('advantage'):
                each_data['advantage'] = each_data['advantage'] + '/' + d1['advantage']
            else:
                each_data = dict(each_data, **d1) 
     
    each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
    each_data['from'] = "58"
    for key,value in each_data.items():
        print('%20s : %s' %(key,value))
       # print(hs)


# for house in houses:

#     print(house)
    # 取节点之后的文本，很有用
    # item = house.xpath('./span[@class="c_ccc"]/node()')
    
    # title = house.xpath('./a')
    # print(title[0].text)
    # print(title[0].get('href'))
    # item = house.xpath('./span[@class="c_ccc"]/following::text()[1]')
    # j = 1
    # for it in item:
        # print(j)
        # j += 1
        # print(it)
        # string = it.xpath('./following::text()[1]')
        # string = it.extract()
        # print(type(string[0]))

    # print(len(item))
   

    # for item in house.xpath('./text()'):
    #     print(j),
    #     print(item)
    #     j += 1

# for title,price,house in zip(titles,prices,houses):
#     each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
#     print("********************************" + str(i))
#     i = i + 1
#     each_data['title'] = title.text
#     each_data['details_url'] = title.get('href')
#     each_data['total_price'] = int(filter(str.isdigit,price.text.encode('utf8')))

#     details = house.xpath('./p')
#     spans = details[0].xpath('./span')
#     for span in spans:
#         string = span.text
#         if string is not None:
#             string = mytools.clearStr(span.text).encode('utf8')
#             d1 = {}
#             d1 = parser.parse_item(string)
#             each_data = dict(each_data, **d1) 
    
#     comms = details[1].xpath('.//a')
#     # print( details[1].xpath('string(.)'))
#     each_data['community_name'] = comms[0].text
    
#     if comms[0].get('href') is None:
#         each_data['comm_url'] = ''
#     else:
#         each_data['comm_url'] = 'http://xm.58.com' + comms[0].get('href')
#     each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
#     each_data['from'] = "58"
    # for key,value in each_data.items():
    #     print('%20s : %s' %(key,value))




# pagelinks = soup.select("ul.pageLink > li > a")

# for link in pages:
    # if link.has_attr('href'):print("http://xm.ganji.com" + link['href'])
    # print(link.get('href'))