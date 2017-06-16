#coding:utf-8
import urllib2
from random import choice
# from spider import html_downloader

class Html_Download(object):

	def __init__(self):

		#设置超时
		# socket.setdefaulttimeout(8)
		
		#从文件中得到代理列表
		with open("Proxies.txt","r") as proxy_file:
			self.proxy_list = proxy_file.readlines()
		
		#从文件中得到浏览器列表
		with open("user_agent.txt","r") as User_agent_file:
			self.agent_list = User_agent_file.readlines()

	def download(self,url,num_retries=3,is_use_header=True):
		print("Downloadding : %s" %(url))
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
		
		try:
			response = urllib2.urlopen(req,timeout=10)
			if response.geturl() != url:
				print(response.geturl())
			html = response.read()
		except urllib2.URLError as e:
			print '			download error:',e.reason,e.code
			html = None
			if num_retries > 0 :
				if hasattr(e,'code') and 500 <= e.code < 600:
					return download(url,num_retries-1)
		return html

# url = r'http://xm.lianjia.com/ershoufang/'
# url = 'http://www.ifeng.com/'
# url = 'http://xm.anjuke.com/sale/?from=navigation#'
url = 'http://xm.maitian.cn/esfall/PG2'
# down = html_downloader.HtmlDownloader()

down = Html_Download()
content = down.download(url)
# print(content)
# print(content)