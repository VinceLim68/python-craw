import PageParser,ToolsBox,Downloader

class GanjiPage(PageParser.PageParser):

    def parse_urls(self, soup):
        new_urls = set()
        pagelinks = soup.select("ul.pageLink > li > a")

        if pagelinks == None:
            print("本页面没有翻页链接。")
        else:
            for link in pagelinks:
                if link.has_attr('href'):
                    new_urls.add("http://xm.ganji.com" + link['href'])

        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        details = soup.select("dd.dd-item.size")
        comms = soup.select(".area")
        # comms = soup.select("dd.dd-item.address > span ")
        prices = soup.select("span.num.js-price")
        titles = soup.select("dd.dd-item.title > a")

        for title, detail, comm, price in zip(titles, details, comms, prices):

            each_data = {'builded_year': 0, 'spatial_arrangement': '', 'floor_index': 0, 'total_floor': 0}
            each_data['title'] = title.get('title')
            each_data['details_url'] = 'http://xm.ganji.com' + title.get('href')
            for item in (detail.stripped_strings):
                d1 = self.parse_item(item)
                each_data = dict(each_data, **d1)

            # 赶集网的小区名称有点混乱，有些嵌套<a>，有些没嵌套
            try:
                c = comm.select('a')
                each_data['community_name'] = c[0].get_text().strip()
                if len(c) >=2:
                    each_data['region'] = c[1].get_text().strip()
                if len(c) >=3:
                    each_data['community_address'] = c[2].get_text().strip()
            except Exception as e:
                c = comm.get_text().split(' - ')
                each_data['community_name'] = c[0].strip()
                if len(c) >=2:
                    each_data['region'] = c[1].strip()
                if len(c) >=3:
                    each_data['community_address'] = c[2].strip()
            each_data['total_price'] = int(round(float(price.get_text()), 0))
            each_data['from'] = "ganji"
            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = GanjiPage()
    url = 'http://xm.ganji.com/fang5/o2/'
    html_cont = downloader.download(url)
    urls,datas = parser.page_parse(html_cont)
    ToolsBox.priList(datas)