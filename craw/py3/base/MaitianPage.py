import PageParser,ToolsBox,Downloader
import re
import datetime
import traceback

class MaitianPage(PageParser.PageParser):

    def parse_urls(self, soup):
        new_urls = set()
        pagelinks = soup.select("#paging > a")

        if pagelinks == None:
            print("本页面没有翻页链接!!")
        else:
            for link in pagelinks:
                if link.get('href') != None:
                    new_urls.add('http://xm.maitian.cn' + link.get('href'))
        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        titles = soup.select("h1 > a")
        infos = soup.select("p.house_info")
        hots = soup.select("p.house_hot")
        areas = soup.select("div.the_area span")
        prices = soup.select("div.the_price span")
        splitby = re.compile(r']|,|\s')

        for title, info, hot, area, price in zip(titles, infos, hots, areas, prices):

            each_data = {'advantage': '', 'builded_year': 0, 'spatial_arrangement': '', 'floor_index': 0,
                         'total_floor': 0}

            each_data['title'] = title.get_text()
            each_data['details_url'] = 'http://xm.maitian.cn' + title.get('href')

            try:
                each_data['total_price'] = ToolsBox.strToInt(price.get_text())
            except Exception as e:
                with open('logtest.txt', 'a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('麦田解析total_price出错，待解析的数据：' + price.get_text())
                    traceback.print_exc(file=fout)
                    print(traceback.format_exc())

            try:
                each_data['block'] = info.get_text().strip()
                each_data['community_name'] = splitby.split(each_data['block'])[-1].strip()
                each_data['block'] = each_data['block'].replace(each_data['community_name'],'')
            except Exception as e:
                with open('logtest.txt', 'a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('Parse Failt of :%s \n' % info.get_text())
                    traceback.print_exc(file=fout)
                    print(traceback.format_exc())

            # try:
                # 麦田的格式，这里是户型、优势和楼层
            temp = ToolsBox.clearStr(hot.text).split('|')
            for item in temp:
                d1 = self.parse_item(item)
                each_data = dict(each_data, **d1)

            # 这是解析面积
            each_data = dict(each_data, **self.parse_item(area.get_text()))

            each_data['from'] = "MT"

            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = MaitianPage()
    url = 'http://xm.maitian.cn/esfall/PG2'
    html_cont = downloader.download(url)
    urls,datas = parser.page_parse(html_cont)
    ToolsBox.priList(datas)