import PageParser,ToolsBox,Downloader

class SfPage(PageParser.PageParser):


    def parse_urls(self, soup):
        new_urls = set()
        links = soup.select("div.fanye > a")
        if links == None :
            print("本页面没有翻页链接。")
        else:
            for link in links:
                if link.get('href') != None:
                    new_urls.add("http://esf.xm.fang.com" + link.get('href'))
        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        titles = soup.select("p.title > a")
        houses = soup.select("dd.info > p.mt12")
        comms = soup.select("p.mt10 > a > span")
        areas = soup.select("div.area.alignR ")
        prices = soup.select("span.price")
        addresses = soup.select(".iconAdress")

        for title, house, comm, area, price,add in zip(titles, houses, comms, areas, prices,addresses):
            each_data = {}

            each_data['title'] = title.get_text()
            each_data['details_url'] = "http://esf.xm.fang.com" + title.get('href')
            each_data['advantage'] = "None"
            each_data['builded_year'] = 0
            each_data['floor_index'] = 0
            for item in list(house.stripped_strings):
                d1 = self.parse_item(item)
                each_data = dict(each_data, **d1)

            each_data['community_name'] = comm.get_text().strip()
            each_data['community_address'] = add.get_text().strip()
            each_data['comm_url'] = comm.parent.get('href')
            each_data['area'] = ToolsBox.strToInt(list(area.stripped_strings)[0])
            each_data['total_price'] = int(float(price.get_text()))
            each_data['from'] = "Soufan"

            each_data = self.pipe(each_data)
            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)


        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = SfPage()
    url = "http://esf.xm.fang.com/"
    html_cont = downloader.download(url)
    # print(type(html_cont))
    urls,datas = parser.page_parse(html_cont)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    # print(datas)
    ToolsBox.priList(datas)
    # ToolsBox.priList(urls)