#coding:utf-8
import traceback  
import datetime

class UrlManager(object):

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self,url):
        if url is None or url.strip() == "":
            return False
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
            return url
        return False


    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        try:
            if len(self.new_urls) != 0:
                new_url = self.new_urls.pop()
                self.old_urls.add(new_url)
                return new_url
        except:
            with open('log.txt','a+') as fout:
                fout.write(str(datetime.datetime.now()) + '\n')
                fout.write("this is in url_manage ,the len of the new_urls is %s \n"%len(self.new_urls))
                traceback.print_exc(file=fout) 
                traceback.print_exc()

    def get_quantity(self):
        return len(self.new_urls),len(self.old_urls)
    
