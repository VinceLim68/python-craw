import PageParser,ToolsBox,Downloader

class WbPage(PageParser.PageParser):

    def is_check(self,soup,type=1):
        # 判断是否是验证界面
        ischeck = soup.select("title")

        if len(ischeck) > 0:            #如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip() if type == 2 else ischeck[0].text
            iscode = (title == "您所访问的页面不存在") or (title == "请输入验证码")
        else:
            iscode = False
        if iscode :
            print('调试：页面标题是---->{0}'.format(title))

        return iscode

    def parse_urls(self, soup):
        new_urls = set()
        pages = soup.select('.pager > a')
        if pages == None :
            print("本页面没有翻页链接。")
        else:
            for link in pages:
                new_urls.add(link.get('href'))
        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        titles = soup.select("h2.title > a")
        prices = soup.select('p.sum > b')
        houses = soup.select('.list-info')

        for title, price, house in zip(titles, prices, houses):
            each_data = {'advantage': '', 'builded_year': 0, 'spatial_arrangement': '', 'floor_index': 0,
                         'total_floor': 0, 'title': title.get_text(), 'details_url': title.get('href'),
                         'total_price': ToolsBox.strToInt(price.get_text())}

            details = house.select('p.baseinfo')
            spans = details[0].select('span')
            for span in spans:
                string = ToolsBox.clearStr(span.get_text()).encode('utf8')
                # d1 = {}
                d1 = self.parse_item(string)
                each_data = dict(each_data, **d1)
            comms = details[1].select('a')
            each_data['community_name'] = comms[0].get_text()

            if comms[0].get('href') is None:
                each_data['comm_url'] = ''
            else:
                each_data['comm_url'] = 'http://xm.58.com' + comms[0].get('href')
            # each_data['price'] = round(float(each_data['total_price'] * 10000 / each_data['area']), 2)
            each_data['from'] = "58"

            try:
                each_data['region'] = comms[1].get_text()
            except Exception as e:
                print('-------这个记录没有拿到小区的区域------------')
                ToolsBox.printDic(each_data)

            try:
                each_data['community_address'] = comms[2].get_text()
            except Exception as e:
                print('-------这个记录没有拿到小区地址------------')
                ToolsBox.printDic(each_data)

            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
                # ToolsBox.printDic(each_data)
                # print('-'*50)
            else:
                if ToolsBox.ShowInvalideData(each_data):page_datas.append(each_data)
        
        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = WbPage()
    url = 'http://xm.58.com/ershoufang/pn2/'
    html_cont = downloader.download(url)
    # print(type(html_cont))
    urls,datas = parser.page_parse(html_cont)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    print(datas)