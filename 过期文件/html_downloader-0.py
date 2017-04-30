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
import gc

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


    def get_content(self,request,retries = 3):
        #打开失败可以重试，并且中间随机停秒
        try:
            response = urllib2.urlopen(request,timeout=10)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
            else:
                data = response.read()
            status = response.getcode()
            if status != 200 and retries > 0:
                print "status code is %s ,You still can try %2.0f times"%(status,retries)
                response.close()
                return self.get_content(request,retries-1)        
            if response.info().getparam("charset") == "gb2312":
                html_cont = data.decode("gbk")
            else:
                html_cont = data               
        except Exception , what :
            print "You still can try " + str(retries) + "times"
            with open('log.txt','a+') as fout:
                fout.write(str(datetime.datetime.now()) + '\n')
                traceback.print_exc(file=fout) 
                traceback.print_exc()
            time.sleep(random.randint(3,7))
            if retries > 0 :
                return self.get_content(request,retries-1)
            else:
                print 'Get Failed',request
                return None 
        finally:
            if 'response' in  dir(): response.close()
            del data
            gc.collect()

        if "anjuke.com" in response.geturl():           #爬取安居客时，有时会给出一些无数据的网页
            soup = BeautifulSoup(html_cont,'html.parser',from_encoding='urf-8')
            houses = soup.find_all(class_="house-details")
            if houses == None :
                print "There is no data from the web"
                time.sleep(random.randint(3,7))
                if retries > 0 :
                    return self.get_content(request,retries-1)
                else:
                    print 'Get Failed',request
                    return None 
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
            
       
        content = self.get_content(req,3)
        
        return content


 

