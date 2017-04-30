#coding:utf-8
import urllib2
from random import choice
url = "http://xm.anjuke.com/sale/p1/?pi=baidu-cpc-xm-tyongxm2&utm_source=baidu&utm_medium=cpc&utm_term=厦门+找房网#filtersort"
with open("user_agent.txt","r") as User_agent_file:
    agent_list = User_agent_file.readlines()
req = urllib2.Request(url)
headers =   {
            "Host":"xm.anjuke.com",
            "Referer":"http://xm.anjuke.com/",
            } 
for key in headers:
    req.add_header(key,headers[key])
            
#得到随机浏览器，并加入头部信息
agent = choice(agent_list).strip('\n')
req.add_header("GET",url)
req.add_header("User-Agent",agent)
#req.add_header('Accept-encoding', 'gzip')

response = urllib2.urlopen(req)
print response.geturl()
# data = response.read()
# print data