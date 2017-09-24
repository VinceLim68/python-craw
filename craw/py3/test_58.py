from base import Downloader,PageParser,ToolsBox
# from bs4 import BeautifulSoup
# import re
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

downloader = Downloader.Downloader()
parser = PageParser.PageParser()
url = 'http://xm.58.com/ershoufang/pn2/'
html_cont = downloader.download(url)
# with open('html_cont.txt','a+') as fout:
#     fout.write(html_cont)
                

# print(html_cont)

soup = parser.get_soup(html_cont,parser_build = 'lxml')

titles = soup.select("h2.title > a")
prices = soup.select('p.sum > b')
houses = soup.select('.list-info')
# print(pages)

i=1

for title,price,house in zip(titles,prices,houses):
    each_data = {'advantage':'','builded_year':0,'spatial_arrangement':'','floor_index':0,'total_floor':0}
    print("********************************" + str(i))
    i = i + 1
    each_data['title'] = title.get_text()
    each_data['details_url'] = title.get('href')
    each_data['total_price'] = ToolsBox.strToInt(price.get_text())

    details = house.select('p.baseinfo')
    spans = details[0].select('span')
    for span in spans:
        string = ToolsBox.clearStr(span.get_text()).encode('utf8')
        d1 = {}
        d1 = parser.parse_item(string)
        each_data = dict(each_data, **d1)
    comms = details[1].select('a')
    each_data['community_name'] = comms[0].get_text()
    
    if comms[0].get('href') is None:
        each_data['comm_url'] = ''
    else:
        each_data['comm_url'] = 'http://xm.58.com' + comms[0].get('href')
    each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
    each_data['from'] = "58"
    ToolsBox.printDic(each_data)
    # for key,value in each_data.items():
    #     print('%20s : %s' %(key,value))

# pages = soup.select('.pager > a')
# for link in pages:
#     print(link.get('href'))
