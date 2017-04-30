#coding:utf-8
from bs4 import BeautifulSoup
import urllib2
from spider import mytools,html_parser
import re 
import datetime
import traceback
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# url = 'http://xm.anjuke.com/sale/p1/'
url = 'http://xm.anjuke.com/sale/rd1?from=zjsr&kw=长青K小区'
response = urllib2.urlopen(url).read()
soup = BeautifulSoup(response,'html.parser',from_encoding='urf-8')
parse = html_parser.HtmlParser()

titles = soup.select("div.house-title > a")
houses = soup.select('div.house-details')
comms = soup.select('span.comm-address')
prices = soup.select('span.price-det')
parse_community = r"(.*)\s*\[(.*)-(.*)\s+(.+)\]"

for title,house,comm,price in zip(titles,houses,comms,prices):
    print '-'*50
    each_data = {}
    each_data['title'] = title.get('title')
    each_data['details_url'] = title.get('href')
    each_data['total_price'] = int(filter(str.isdigit,price.get_text().encode('utf8')))
    

    try:
        each_data['community_name'],each_data['region'],each_data['block'],each_data['community_address'] = re.findall(parse_community,comm.get('title'))[0]
    except Exception, e:
        with open('logtest.txt','a+') as fout:
            fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
            fout.write('Parse Failt of :%s \n'%comm.get('title'))
            traceback.print_exc(file=fout) 
            print traceback.format_exc()

    house1 = house.stripped_strings
    for item in house1:
        item = item.replace('<br/>','').replace('\r\n','').replace(' ','')
        if u'层' in item and len(item) < 12:
            try:
                each_data['floor_index'],each_data['total_floor'] = parse.parse_floor(item,'(')
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    for i2 in house1:
                        fout.write(i2)
                    fout.write('\now')
                    fout.write('Parse Failt of THE FLOOR:%s \n'%item.encode('utf8'))
                    fout.write(each_data['details_url'])
                    fout.write(str(house))
                    traceback.print_exc(file=fout) 
                    print (traceback.format_exc())
        if u'年' in item and len(item) < 12:
            try:
                each_data['builded_year'] = int(filter(str.isdigit,item.encode('utf8')))
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('Parse Failt of THE YEAR:%s \n'%item.encode('utf-8'))
                    traceback.print_exc(file=fout) 
                    print traceback.format_exc()
        if u'室' in item and len(item) < 12:
            each_data['spatial_arrangement'] = item.strip()
        if U'平方米' in item and U'元' not in item and len(item) < 12:
            try:
                each_data['area'] = round(float(item.split('平'.decode('utf-8'))[0]),0) 
            except Exception, e:
                with open('logtest.txt','a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('Parse Failt of THE AREA:%s \n'%item.encode('utf-8'))
                    traceback.print_exc(file=fout) 
                    print traceback.format_exc()
    each_data['price'] = round(each_data['total_price']*10000/each_data['area'],0)
    each_data['from'] = "AJK" 
    for key,value in each_data.items():mytools.pri( " %s : %s"%(key,value))

    
