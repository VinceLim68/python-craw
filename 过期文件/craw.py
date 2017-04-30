#coding:utf-8
#这是持续抓取挂牌记录的程序
from spider import url_manager,html_downloader,AJK_parser,html_outputer,myStat,SF_parser
import urllib
import time,random


class SpiderMain(object):
    def __init__(self,parseClass):
        self.urls = url_manager.UrlManager()
        self.comms = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = parseClass
        self.outputer = html_outputer.HtmlOutputer()
        self.count = 1
        self.count1 = 1
        self.total = 0

    def craw(self,root_url,keywords,from_):
        #self.count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():                     
            try:
                new_url = self.urls.get_new_url()
                #print ('craw %d : %s' %(count,new_url))
                print ('craw %d :' %(self.count))
                html_cont = self.downloader.download(new_url,False,True)
                # print "download ok!"
                # print html_cont
                new_urls,new_datas,new_comms = self.parser.parse(html_cont,from_)
                #print "parser Ok"
                self.urls.add_new_urls(new_urls)
                self.comms.add_new_urls(new_comms)
                self.outputer.collect_data(new_datas,keywords)
                quantity_of_raw_datas = len(self.outputer.get_raw_datas())
                quantity_of_datas = len(self.outputer.get_datas())
                quantity_of_dupli = self.outputer.get_dupli_count()
                print "**%6.0f = %6.0f dupli + %6.0f raw_datas + %6.0f stored , %6.0f datas in list **"\
                %(quantity_of_dupli + quantity_of_raw_datas + self.total,quantity_of_dupli,quantity_of_raw_datas,self.total,quantity_of_datas )
                self.count = self.count + 1
            except Exception as e:
                print ('craw failed :' + str(e))
        return

    def craw_control(self,from_where):

        #*while self.urls.has_new_comm() :
        while self.comms.has_new_url:
            try:
                new_comm = str(self.comms.get_new_url().strip())
                quantity_of_new_comms,quantity_of_old_comms = self.comms.get_quantity()
                quantity_of_raw_datas = len(self.outputer.get_raw_datas())

                try:
                    print "********** %s :Crawing %s **************"%(self.count1,unicode(new_comm,"utf-8").encode("gbk"))
                except:
                    print "********** %s :Crawing **************"%(self.count1)
                print "Now there is %5.0f communities for craw, %5.0f has been crawed,%6.0f raw_datas in list,%6.0f records stored in MySQL" \
                %(quantity_of_new_comms,quantity_of_old_comms,quantity_of_raw_datas,self.total)
                #time.sleep(random.randint(5,7))
                if from_where == 1:
                    serch_for = urllib.quote(new_comm)
                    search_url = 'http://xm.anjuke.com/sale/p1-rd1/?kw=' + serch_for + '&from_url=kw_final#filtersort'
                if from_where == 3:
                    search_url = 'http://esf.xm.fang.com/house/c61-kw' + urllib.quote(unicode(new_comm,"utf-8").encode('gbk')) +'/'
                self.craw(search_url,new_comm,from_where)
                self.count1 = self.count1 + 1
                if quantity_of_raw_datas >= 3000:
                    print "try to store"
                    self.total = self.total + self.outputer.out_mysql()
                    self.outputer.clear_datas()
            except:
                self.outputer.out_mysql()
                self.outputer.clear_datas()
        self.outputer.out_mysql()
        self.outputer.clear_datas()

       

if __name__=="__main__":

    from_where = 1
    if from_where == 1:
        root_url = "http://xm.anjuke.com/sale/p1/#filtersort"
        obj_spider = SpiderMain(AJK_parser.AjkParser())
    if from_where == 3:
        root_url = "http://esf.xm.fang.com/"
        obj_spider = SpiderMain(SF_parser.SfParser())
    obj_spider.craw(root_url,"*",from_where)
    #obj_spider.pri_info()
    obj_spider.craw_control(from_where)

    



