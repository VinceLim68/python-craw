#coding:utf-8
from random import choice

class ReqBuilder(object):
    """单例"""
    
    __instance = None

    
    def __init__(self):
        # 从文件中得到代理列表,这个文件是根目录下而不是/spider目录下
        with open("Proxies.txt","r") as proxy_file:
            self.proxy_list = proxy_file.readlines()
        #从文件中得到浏览器列表
        with open("user_agent.txt","r") as User_agent_file:
            self.agent_list = User_agent_file.readlines()

    def __new__(cls,*args,**kwd):
        if ReqBuilder.__instance is None:
            ReqBuilder.__instance=object.__new__(cls,*args,**kwd)
        return ReqBuilder.__instance

    """
        代理的格式
        proxies = {
          "http": "http://10.10.1.10:3128",
          "https": "http://10.10.1.10:1080",
        }
    """
    def get_proxy(self):
        ip = choice(self.proxy_list).strip('\n')
        proxy = {'http':'http://' + ip}
        return proxy

    def get_agent(self):
        agent = choice(self.agent_list).strip('\n')
        return agent

if __name__=="__main__":
    r1 = ReqBuilder()
    print(r1.get_proxy())
    print(r1.get_agent())
