#coding:utf-8
import xlsxwriter
import sys
from spider import html_downloader
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

downloader = html_downloader.HtmlDownloader()
url = 'http://tz.xmtfj.gov.cn/jyjg_19.xhtml?a=&y='
html_cont = downloader.download(url,False,True)
soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')

records = soup.select("table.tab4 > tr")
lands = []

for record in records:
	# print('8'*50)
	data = {}
	r2 = record.select('td')
	data['landNo'] = (r2[0].contents[0].get('title').encode("utf-8"))
	data['href'] = (r2[0].contents[0].get('href'))
	data['use'] = (r2[1].contents[1].get('title').encode("utf-8"))
	data['address'] = (r2[2].contents[0].get('title').encode("utf-8"))
	data['date'] = (r2[3].get('title').encode("utf-8"))
	data['acreage'] = (r2[4].get('title').encode("utf-8"))
	data['floorArea'] = (r2[5].get('title').encode("utf-8"))
	data['price'] = (r2[6].get_text().encode("utf-8"))
	data['user'] = (r2[7].get('title').encode("utf-8"))

	lands.append(data)




fout = xlsxwriter.Workbook('lands.xlsx')
worksheet = fout.add_worksheet('')
amount = 0  #记录总数
row = 1     #记录行
title = ['地块编号','地块用途','土地位置','成交日期','土地面积','建筑面积','成交价','受让人','楼面价','备注']
worksheet.write_row('A1',title)
url_format = fout.add_format({
    'font_color': 'blue',
    'underline':  1
})
# worksheet.write_url(1, 0 , 'http://www.python.org/', url_format, 'Your text here')
row = 1
worksheet.set_column('A:A', 10)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 50)
worksheet.set_column('D:G', 12)
worksheet.set_column('H:H', 20)
worksheet.set_column('I:I', 12)
worksheet.set_column('J:J', 80)
for i in lands:
	worksheet.write_url(row, 0 , data['href'], url_format, data['landNo'])
	worksheet.write(row,1,data['use'])
	worksheet.write(row,1,data['address'])
	worksheet.write(row,1,data['date'])
	worksheet.write(row,1,data['acreage'])
	worksheet.write(row,1,data['floorArea'])
	worksheet.write(row,1,data['price'])
	worksheet.write(row,1,data['user'])
	row += 1


fout.close()