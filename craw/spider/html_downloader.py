#coding:utf-8
import urllib2
import socket
from random import choice
import time,random
from StringIO import StringIO
import gzip
from bs4 import BeautifulSoup
import traceback  
import datetime
import mytools

class HtmlDownloader(object):

    def __init__(self):

        #设置超时
        socket.setdefaulttimeout(8)

        #从文件中得到代理列表,这个文件是根目录下而不是/spider目录下
        with open("Proxies.txt","r") as proxy_file:
            self.proxy_list = proxy_file.readlines()
        #从文件中得到浏览器列表
        with open("user_agent.txt","r") as User_agent_file:
            self.agent_list = User_agent_file.readlines()



    # @mytools.mylog             #2016.6.1使用装饰器处理错误信息,但是不知道为什么，加上装饰器会返回none
    def get_content(self,request,retries = 3):

        # 打开失败可以重试，并且中间随机停秒

        try:
            response = urllib2.urlopen(request,timeout=10)
            # print('open ok')
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
            else:
                data = response.read()
            status = response.getcode()
            
            if status != 200 and retries > 0:
                print('status is %s and retries is %s' %(status,retries))
                html_cont = None

            if response.info().getparam("charset") == "gb2312":
                html_cont = data.decode("gbk")
            else:
                html_cont = data
        except Exception as e :
        # except urllib2.URLError as e:
            # print('error now %s' %e)
            html_cont = None
            with open('logtest.txt','a+') as fout:      #2017.3把错误日志改成logtest.txt
                fout.write('\n*******get_content urlopen error record by get_content ' + str(datetime.datetime.now()) + '*************\n')
                fout.write(str(datetime.datetime.now()) + '\n')
                traceback.print_exc(file=fout)
                print traceback.format_exc()
            
            # print(e)
            # print('*'*80)
            # time.sleep(15)
            # 被禁止时，返回404
            if hasattr(e, 'code') and e.code == 404:
                html_cont = 404 
            #出现服务器错误时可以重新连接
            elif retries > 0:
                # print("You are still have " + str(retries) + "times to try open this url")
                time.sleep(random.randint(3,7))
                return self.get_content(request, retries - 1)

        finally:
            if 'response' in  dir(): response.close()

        return html_cont


    def download(self,url,is_use_proxy,is_use_header):

        if url is None:
            return None

        if is_use_proxy:
            #得到随机代理，但每个单元会多一个换行符，用strip('\n')把它去掉
            ip = choice(self.proxy_list).strip('\n')
            proxy = {'http':'http://' + ip}
            proxy_support = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            print "Ip "+ ip + "  try to open :" + url
        else:
            #前面因为已经建立了代理，这里是继续使用原来的代理，而不是不用代理
            print " Try to open : " + url 

        req = urllib2.Request(url)


        if is_use_header:
            headers = {}
            if "anjuke.com" in url:
                headers =   {
                        "Host":"xm.anjuke.com",
                        "Referer":"http://xm.anjuke.com/",
                        }  

            if "xmhouse.com" in url:
                headers = {
                        "Host":"esf.xmhouse.com",
                        "Referer":"http://esf.xmhouse.com/",
                }

            if ".fang.com" in url:
                headers = {
                        "Host":"esf.xm.fang.com",
                        "Origin":"http://esf.xm.fang.com",
                        "Referer":"http://esf.xm.fang.com/"
                }
                req.add_header('Accept-encoding', 'gzip')

            if ".lianjia.com" in url:
                headers = {
                        # "Host":"xm.lianjia.com",  
                        # "Referer":"https://xm.lianjia.com/ershoufang/"
                    'Accept':'text/html, application/xhtml+xml, */*',
                    'Referer':'https://xm.lianjia.com/ershoufang/rs%E6%B3%89%E6%B0%B4%E6%B9%BE%E4%B8%80%E6%9C%9F/',
                    'Accept-Language':'zh-CN',
                    'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
                    'Accept-Encoding':'deflate',        #//这个会造成抓取失败
                    'Host':'xm.lianjia.com',
                    'Connection':'Keep-Alive',
                    'Cookie':'lianjia_uuid=5bf6b14a-8b3c-437c-a52d-ceb68ff9f161; UM_distinctid=15adef6e3341b5-062bb019e-4349052c-140000-15adef6e3354ed; select_city=350200; _jzqckmp=1; all-lj=eae2e4b99b3cdec6662e8d55df89179a; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503302867,1503306127,1503387026,1503468661; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503470994; CNZZDATA1255847100=932838031-1469061064-%7C1503467486; _jzqa=1.4030431236783739000.1469062989.1503468661.1503470994.56; _jzqc=1; _jzqx=1.1479358284.1503470994.7.jzqsr=xm%2Elianjia%2Ecom|jzqct=/ershoufang/pg82/.jzqsr=xm%2Elianjia%2Ecom|jzqct=/ershoufang/rs%e6%b3%89%e6%b0%b4%e6%b9%be%e4%b8%80%e6%9c%9f/; _smt_uid=57901f4c.225c23b5; CNZZDATA1254525948=1901811509-1469058879-%7C1503470771; _jzqb=1.1.10.1503470994.1; CNZZDATA1255633284=618103687-1469058318-%7C1503467205; _qzja=1.1871061607.1469062988780.1503468660915.1503470993690.1503468712703.1503470993690..0.0.139.56; _qzjb=1.1503470993690.1.0.0.0; _qzjc=1; _qzjto=3.2.0; CNZZDATA1255604082=1618345746-1469059066-%7C1503469466; _gat=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1409175644.1469062989; _gid=GA1.2.1387427048.1503277191; _gat_dianpu_agent=1; lianjia_ssid=554a1964-c1e2-4e69-9de1-0da6a67e88e3'
                }

            for key in headers:
                req.add_header(key,headers[key])

            #得到随机浏览器，并加入头部信息
            agent = choice(self.agent_list).strip('\n')
            req.add_header("GET",url)
            req.add_header("User-Agent",agent)
            print('User-Agent : %s' %agent)

        content = self.get_content(req)

        return content





 



