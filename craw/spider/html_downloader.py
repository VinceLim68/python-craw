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
        #从文件中得到代理列表
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
                html_cont - None

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

            for key in headers:
                req.add_header(key,headers[key])

            #得到随机浏览器，并加入头部信息
            agent = choice(self.agent_list).strip('\n')
            req.add_header("GET",url)
            req.add_header("User-Agent",agent)

        content = self.get_content(req)

        return content





 



