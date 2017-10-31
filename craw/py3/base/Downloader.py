import requests
# from random import choice
# import socket

# 这几条应该放在程序的主入口
import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

# import urllib.request
# from spider import html_downloader

class Downloader(object):

    # def __init__(self,headers={},proxy=None):

    #     self.headers = headers  
    #     self.proxy = proxy

    # 下载主体
    # 支持延时，文件头，代理，重复抓取
    def download(self,url,headers={},proxy=None,num_retries=3):
        
        print("Downloadding : {0}".format(url))
        
        try:
            r = requests.get(url = url, headers = headers, 
                timeout = 8, proxies = proxy)
            if 400 <= r.status_code <500:
                html = 404
            elif 500 <= r.status_code <600:         #递归:服务器端出错时
                if num_retries > 0:
                    print('服务器瑞出现问题，将再下载{0}次'.format(num_retries-1))
                    html = self.download(url,num_retries-1)
                else:
                    html = None
            else:
                # requests 在解析页面时，如果title没有声明charset,会默认使用'ISO-8859-1'，造成解码错误
                if r.encoding == 'ISO-8859-1':
                    html = r.text.encode('ISO-8859-1').decode(r.apparent_encoding)
                else:
                    html = r.text
        except Exception as e:
            print("Request failed(在Downloader里): {0}".format(e))
            html = None

        # print('r.headers["content-type"]is {0}'.format(r.headers['content-type']))
        # print('r.encoding is {0}'.format(r.encoding))
        # print('r.apparent_encoding is {0}'.format( r.apparent_encoding))

        return html



if __name__=="__main__":
    # print('qqqqqq')
    url = r'http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html'
    # url = "http://esf.xm.fang.com/"
    # url = 'http://www.234.com'
    # url = 'http://xm.58.com/ershoufang/?key=金彩花苑'
    # url = 'http://www.ifeng.com/'
    # url = 'http://xm.anjuke.com/sale/?from=navigation#'
    # url = 'http://xm.maitian.cn/esfall/PG2'
    # down = html_downloader.HtmlDownloader()
    # headers = {
    # 'Accept':'text/html, application/xhtml+xml, */*',
    # 'Referer':'https://xm.lianjia.com/ershoufang/rs%E6%B3%89%E6%B0%B4%E6%B9%BE%E4%B8%80%E6%9C%9F/',
    # 'Accept-Language':'zh-CN',
    # 'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
    # 'Accept-Encoding':'gzip,deflate',        #//这个会造成抓取失败
    # 'Host':'xm.lianjia.com',
    # 'Connection':'Keep-Alive',
    # # 'Cookie':'lianjia_uuid=5bf6b14a-8b3c-437c-a52d-ceb68ff9f161; UM_distinctid=15adef6e3341b5-062bb019e-4349052c-140000-15adef6e3354ed; select_city=350200; _jzqckmp=1; all-lj=eae2e4b99b3cdec6662e8d55df89179a; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503302867,1503306127,1503387026,1503468661; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503470994; CNZZDATA1255847100=932838031-1469061064-%7C1503467486; _jzqa=1.4030431236783739000.1469062989.1503468661.1503470994.56; _jzqc=1; _jzqx=1.1479358284.1503470994.7.jzqsr=xm%2Elianjia%2Ecom|jzqct=/ershoufang/pg82/.jzqsr=xm%2Elianjia%2Ecom|jzqct=/ershoufang/rs%e6%b3%89%e6%b0%b4%e6%b9%be%e4%b8%80%e6%9c%9f/; _smt_uid=57901f4c.225c23b5; CNZZDATA1254525948=1901811509-1469058879-%7C1503470771; _jzqb=1.1.10.1503470994.1; CNZZDATA1255633284=618103687-1469058318-%7C1503467205; _qzja=1.1871061607.1469062988780.1503468660915.1503470993690.1503468712703.1503470993690..0.0.139.56; _qzjb=1.1503470993690.1.0.0.0; _qzjc=1; _qzjto=3.2.0; CNZZDATA1255604082=1618345746-1469059066-%7C1503469466; _gat=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1409175644.1469062989; _gid=GA1.2.1387427048.1503277191; _gat_dianpu_agent=1; lianjia_ssid=554a1964-c1e2-4e69-9de1-0da6a67e88e3'
    # }

    # headers = {
    #     'Accept':'text/html, application/xhtml+xml, */*',
    #     'Accept-Language':'zh-CN',
    #     'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
    #     'Accept-Encoding':'gzip, deflate',
    #     'Host':'xm.58.com',
    #     'Connection':'Keep-Alive',
    #     # 'Cookie':'bangbigtip2=1; f=n; id58=c5/nn1eXLAxDpemLKp4DAg==; bj58_id58s="RW52WjJGMXNzSTMxNDE1MA=="; bdshare_firstime=1479370463887; tj_ershoubiz=true; bj58_new_uv=4; 58home=xm; als=0; commontopbar_myfeet_tooltip=end; final_history=641251%2C844280; ppStore_fingerprint=BF49DD3F0EFD254891AB944E01811768FC16A47947ED9328%EF%BC%BF1503299536233; ipcity=xm%7C%u53A6%u95E8%7C0; city=xm; XQH=%7B%22w%22%3A%5B%7B%22id%22%3A%22653163%22%2C%22t%22%3A1502702580455%7D%2C%7B%22id%22%3A%22642439%22%2C%22t%22%3A1503303414539%7D%2C%7B%22id%22%3A%22641376%22%2C%22t%22%3A1503307125841%7D%2C%7B%22id%22%3A%22641937%22%2C%22t%22%3A1503307136217%7D%2C%7B%22id%22%3A%22844231%22%2C%22t%22%3A1503326003430%7D%2C%7B%22id%22%3A%22893456%22%2C%22t%22%3A1503458370824%7D%5D%7D; Hm_lvt_ae019ebe194212c4486d09f377276a77=1502702581,1503303415,1503326004,1503458374; Hm_lpvt_ae019ebe194212c4486d09f377276a77=1503458374; __utma=253535702.389478886.1469758150.1503326004.1503458387.27; __utmc=253535702; __utmz=253535702.1503458387.27.21.utmcsr=xm.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/ershoufang/; xxzl_deviceid=DQevm4nNXuo9PMVG%2BNgkMxPtgIef%2Brda40ndWcUirqiaL9bEoxOloNXhfg%2BZZPCP; 58tj_uuid=d94e7310-bff6-4e62-9c19-36d5b6e6585d; new_session=0; new_uv=54; utm_source=; spm=; init_refer=; commontopbar_city=606%7C%u53A6%u95E8%7Cxm'
    #     }
    down = Downloader()
    content = down.download(url)
    # print(content.encode('GB18030'))
    print(content)
    # print(sys.getdefaultencoding())
    # r = requests.get(url)
    # resp = requests.get(url=url)
    # print 'resp', resp.cookies._cookies
    # print 'req',  resp.request._cookies._cookies

    # s= requests.Session()#自动处理cookie
    # r = s.get(url)
    # print(r.text)
    # # # print(r.headers)
    # print(r.request.headers)
    # print(r.request._cookies._cookies)
    # print(r.text)
    # print(content)