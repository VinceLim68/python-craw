import PageParser,ToolsBox,Downloader
import re

class LjPage(PageParser.PageParser):

    def is_check(self,soup):
        # 判断是否是验证界面
        ischeck = soup.select("title")
        if len(ischeck) > 0:            # 如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip()
            iscode = title == "验证异常流量-链家网"
        else:
            iscode = False

        if iscode :
            print('调试：页面标题是---->{0}'.format(title))
        return iscode

    def parse_urls(self, soup):
        new_urls = set()
        links = soup.select("div.house-lst-page-box")
        if links == None :
            print("本页面没有翻页链接。")
        else:
            t_page = eval(links[0].get('page-data'))['totalPage']
            url = links[0].get('page-url')
            for i in range(1, t_page + 1):
                new_urls.add("http://xm.lianjia.com" + url.replace("{page}", str(i)))
        return new_urls

    def parse_datas(self,soup):
        page_datas = []

        titles = soup.select("div.title > a")
        houseinfo = soup.select("div.houseInfo")
        positionInfo = soup.select("div.positionInfo")
        totalprices = soup.select("div.totalPrice")
        for title, info, position, totalPrice in zip(titles, houseinfo, positionInfo, totalprices):
            each_data = {'builded_year': 0, 'spatial_arrangement': '', 'floor_index': 0, 'total_floor': 0}
            each_data['title'] = title.get_text()
            each_data['details_url'] = title.get('href')
            each_data['total_price'] = int(
                round(float(re.search('(\d+.?\d+)万', totalPrice.get_text()).groups(0)[0]), 0))

            info_item = (info.get_text().split('|'))

            each_data['community_name'] = info_item[0].strip()  # 第1个总是小区名称
            for i in range(1, len(info_item)):
                d1 = self.parse_item(info_item[i].strip())
                if ('advantage' in each_data.keys()) and ('advantage' in d1.keys()):
                    d1['advantage'] = each_data['advantage'] + ',' + d1['advantage']
                each_data = dict(each_data, **d1)

            position = position.get_text().replace('\t', '').replace('\n', '').split()
            each_data['block'] = position[-1]

            if ')' not in position[0]:  # 链前的别墅会用'4层2008年建'的形式，加入')'，以便分隔
                position[0] = position[0].replace('层', '层)')

            for item in position[0].split(')'):  # 2017.4.1链家格式有改
                d1 = self.parse_item(item.strip())  # 2017.4.1链家格式有改
                each_data = dict(each_data, **d1)

            each_data['from'] = "lianjia"

            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = LjPage()
    url = "http://xm.lianjia.com/ershoufang/pg1/"
    html_cont = downloader.download(url)
    # print(type(html_cont))
    urls,datas = parser.page_parse(html_cont)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    # print(datas)
    ToolsBox.priList(urls)
    # ToolsBox.priList(urls)