#coding:utf-8
#网络物业信息爬虫4.0，模块化，遇错不停止
#加入厦门房地产联合网解析
#加入代理功能
#把解析里的面积、单价、总楼层、建成年份都转换成数字；输出的数据分为抓取到的、和清洗后的。
#单价直接计算入库，增加按小区关键字抓取
#可以批量采集xmhouse挂牌信息
#把不同网站的解析拆成不同的类
#增加soufan、Qfan
#对Qfan中第几层解析错误进行了修改,Qfang面积采用取整
#引进将错误信息输出到日志
#试图处理下载网页时的超时现象
from __future__ import print_function
from spider import url_manager,html_downloader,html_outputer,AJK_parser,XM_parser,SF_parser,QF_parser,LJ_parser,mytools,WB_parser
import urllib         #2016.5.30取消不必要的包
import datetime
import sys
from urllib import quote
import traceback  
import data_stat
import time,random
from random import choice

# from guppy import hpy


class SpiderMain(object):
    def __init__(self,parseClass):
        self.urls = url_manager.UrlManager()
        self.comms = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = parseClass
        self.outputer = html_outputer.HtmlOutputer()
        self.data_stat = data_stat.DataStat()
        self.count = 1
        self.total = 0
        self.quantity_of_raw_datas = 0
        # self.hp = hpy()
        self.quantity_of_dupli = 0
        self.quantity_of_datas = 0
        
        #连续出现几个页面没有数据的暂停
        self.nodata = 0             
        self.nodata_pages_stop = 5
        
        #连续出现几个404的暂停
        self.forbidden = 0
        self.forbidden_pages_stop = 2
        
        # 设置延时
        if 'AjkParser' in str(parseClass):
            self.delay = 3
        elif 'GjParser' in str(parseClass):
            self.delay = 3
        elif 'LjParser' in str(parseClass):
            self.delay = 3
        elif 'LejuParser' in str(parseClass):
            self.delay = 3
        else:
            self.delay = 0


    def craw(self,root_url,keywords,from_):
        # 先把第一个root_url加入urls列表中,支持root_url有多个url
        for url in root_url:
            self.urls.add_new_url(url)
        
        # 开始循环抓取数据
        while self.urls.has_new_url() :
            # 取出一个页面
            new_url = self.urls.get_new_url()
            # if from_ == '8':print(new_url)
            # 抓取一个页面
            self.craw_oneurl(new_url,keywords,from_)
        self.print_record()

    def print_record(self):
        #专门在日志里记录已经获取记录数的模块
        with open('logtest.txt','a+') as fout:
            fout.write('\n*******' + str(datetime.datetime.now()) + '*************')
            fout.write( '\n %9.0f records has been stored in MySQL ' %self.total)

    @mytools.mylog
    @mytools.exeTime
    def craw_oneurl(self,new_url,keywords,from_,retries = 3):
        
        # 把取url移到外面，可以针对同一链接循环解析
        
        if self.delay > 0 :
            sleepSeconds = random.randint(self.delay,self.delay*2)
            print ('craw %d after %d seconds (%d ~ %d):' %(self.count,sleepSeconds,self.delay,self.delay*2))
        else:
            print ('craw %d :' %(self.count))
        
        html_cont = self.downloader.download(new_url,False,True)
        
        if html_cont == 404:                    #增加对被禁ip的处理
            self.forbidden += 1
            time.sleep(30*self.forbidden)      #被禁止访问了，消停一会
            if self.forbidden > self.forbidden_pages_stop:
                raw_input('It seems you have been forbidden,press any key to continue......')
                self.forbidden = 0
            # 2017.5.11增加404情况回调
            else:
                return self.craw_oneurl(new_url,keywords,from_)
        
        elif html_cont is not None:
            
            if from_ == '8' and keywords != '*':
                # 58同城按小区搜索的挂牌信息
                new_urls,new_datas = self.parser.parseB(html_cont)
            else:
                new_urls,new_datas = self.parser.parse(html_cont,from_)
            
            # new_urls,new_datas = self.parser.parse(html_cont,from_)

            # 如果是验证界面，得到延时值，回调函数
            if new_datas == 'checkcode':
                self.delay = int(new_urls)               # 调整延时值
                if retries > 0:
                    return self.craw_oneurl(new_url,keywords,from_,retries - 1)
            
            # 当解析没有得到数据时，我怀疑是网络问题，再解析一次，但超过nodata_pages_stop次数则暂停
            elif len(new_datas) == 0 and len(new_urls) == 0:
                with open('logtest.txt','a+') as fout:
                    fout.write('\n*******' + str(datetime.datetime.now()) + '*************')
                    fout.write( '\n no new datas have been crawed :%s. \n' %new_url)
                print(' There are %s datas and %s urls in %s' %(len(new_datas),len(new_urls),new_url))
                self.nodata += 1                #只有连续5个页面没有数据才会停止
                
                if self.nodata < self.nodata_pages_stop:
                    print("You are still have " + str(self.nodata_pages_stop-self.nodata) + "times to parse this url") 
                    time.sleep(random.randint(3,7))
                    # return self.craw_oneurl(new_url,keywords,from_, retries - 1)
                    return self.craw_oneurl(new_url,keywords,from_)
            
            # 正常情况，解析
            else:
                # 取页码表
                self.urls.add_new_urls(new_urls)

                # 取小区表，但58的不取了

                if from_ != '8' :
                    self.comms.add_new_urls([name['community_name'] for name in new_datas]) 
                elif keywords == '*':
                    self.comms.add_new_urls([name['comm_url'] for name in new_datas])
                
                # self.comms.add_new_urls([name['community_name'] for name in new_datas]) 

                self.outputer.collect_data(new_datas,keywords)
                self.quantity_of_datas,self.quantity_of_raw_datas,self.quantity_of_dupli = self.outputer.get_datas_quantity()
                print("  %6.0f = %6.0f dupli + %5.0f raw_datas + %6.0f stored , %5.0f in list"\
                %(self.quantity_of_dupli + self.quantity_of_raw_datas + self.total,self.quantity_of_dupli,self.quantity_of_raw_datas,self.total,self.quantity_of_datas ))
                if self.quantity_of_raw_datas > 3000:
                    print ("try to store")
                    self.total = self.total + self.outputer.out_mysql()
                    self.outputer.clear_datas()
                self.count += 1
                self.nodata = 0             #如果有数据，把self.nodata计数器清零
                self.forbidden = 0          #如果有数据，把self.forbidden计数器清零
        
        # html_cont内容是None
        else:
            print('craw %s fail : nothing' %(new_url))

        # 延时模块：放在最后，第一次抓取时不用延时
        if self.delay > 0 :
            time.sleep(sleepSeconds)             #2017.5。15把下载延时功能放在这里，这个模块相当于控制器


    @mytools.mylog
    def out(self,from_):
        if keywords != "*":
            v2 = self.data_stat.get_anlyse(keywords,self.outputer.get_datas())
            print(self.data_stat.info)            
            self.outputer.out_xlsx(keywords,from_)
        if "home" not in sys.path[0]:
            self.total = self.outputer.out_mysql()

if __name__=="__main__":
    keywords = '红树康桥'
    serch_for = quote(keywords)
    from_where = 6

    #1----安居客，2----XMHOUSE，3--搜房网，4----Q房网，5----链家

    if from_where == 1:
        root_url = ['http://xm.anjuke.com/sale/p1-rd1/?kw=' + serch_for + '&from_url=kw_final#filtersort']
        obj_spider = SpiderMain(AJK_parser.AjkParser())
    if from_where == 2:
        root_url = ['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_1.html'] if keywords == '*' \
                else ['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s1_itp_b0_it_if_ih1_p-_ar-_pt_o0_ps20_1.html?keyWord=' + serch_for ]
        obj_spider = SpiderMain(XM_parser.XmParser())
    if from_where == 3:
        root_url = ['http://esf.xm.fang.com/house/c61-kw' + urllib.quote(unicode(keywords,"utf-8").encode('gbk')) +'/']
        obj_spider = SpiderMain(SF_parser.SfParser())
    if from_where == 4:
        root_url = ['http://xiamen.qfang.com/sale/f1','http://xiamen.qfang.com/sale/f2'] if keywords == '*' \
                else ["http://xiamen.qfang.com/sale/f1?keyword=" + serch_for,"http://xiamen.qfang.com/sale/f2?keyword=" + serch_for]
        obj_spider = SpiderMain(QF_parser.QfParser())
    if from_where == 5:
        root_url = ['http://xm.lianjia.com/ershoufang/pg1/'] if keywords == '*' \
                else ["http://xm.lianjia.com/ershoufang/rs" + serch_for]
        obj_spider = SpiderMain(LJ_parser.LjParser())
    if from_where == 6:
        root_url = ['http://xm.ganji.com/fang5/o1/'] 
        obj_spider = SpiderMain(LJ_parser.LjParser())

    obj_spider.craw(root_url,keywords,from_where)
    obj_spider.out(from_where)


