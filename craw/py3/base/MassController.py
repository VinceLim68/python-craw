#coding:utf-8
import UrlManager,ToolsBox,Downloader,Outputer,ReqBuilder
from random import choice
import time,random
# from __future__ import print_function
# from spider import url_manager,html_downloader,html_outputer,AJK_parser,XM_parser,SF_parser,QF_parser,LJ_parser,mytools,WB_parser
# import urllib         #2016.5.30取消不必要的包
# import datetime
# import sys
# from urllib import quote
# import traceback  
# import data_stat

# from guppy import hpy


class MassController(object):
    def __init__(self,parseClass):
        
        self.urls = UrlManager.UrlManager()             #url管理
        # self.comms = UrlManager.UrlManager()            #小区管理
        self.downloader = Downloader.Downloader()       #下载器
        self.parser = parseClass
        # self.outputer = Outputer.Outputer()
        self.rqBuilder = ReqBuilder.ReqBuilder()
        
        self.headers = {}                               #构筑请求头
        self.HTTP404 = 0                                #计数：被404的次数
        self.HTTP404_stop = 3                           #设置：累计404多少次后暂停程序
        self.retry_times = 3                            #设置：下载失败后重试的次数
        self.count = 1                                  #计数：下载页面数
        self.delay = 3                                  #设置：下载页面之间的延时秒数
        # self.total = 0
        # self.quantity_of_raw_datas = 0
        # # self.hp = hpy()
        # self.quantity_of_dupli = 0
        # self.quantity_of_datas = 0
        
        # #连续出现几个页面没有数据的暂停
        # self.nodata = 0             
        # self.nodat_stop = 5
        
        # #连续出现几个404的暂停
        # self.HTTP404 = 0
        # self.HTTP40_stop = 2
        
        # # 设置延时
        # if 'AjkParser' in str(parseClass):
        #     self.delay = 3
        # elif 'GjParser' in str(parseClass):
        #     self.delay = 3
        # elif 'LjParser' in str(parseClass):
        #     self.delay = 3
        # # elif 'WBParser' in str(parseClass):
        # #     self.delay = 2
        # elif 'LejuParser' in str(parseClass):
        #     self.delay = 3
        # else:
        #     self.delay = 0


    def headers_builder(self):
        # 构建请求头信息
        agent = self.rqBuilder.get_agent()
        self.headers["User-Agent"] = agent

    def proxy_builder(self):
        # 构建代理信息
        return self.rqBuilder.get_proxy()
        
    def craw_controller(self,root_url):
        
        # 1、把root_url加入urls列表中,支持root_url有多个url
        for url in root_url:
            self.urls.add_new_url(url)
        
        # 2、循环抓取数据
        while self.urls.has_new_url() :
            url = self.urls.get_new_url()
            self.craw_a_page(url)
        
    #     self.print_record()

    # def print_record(self):
    #     #专门在日志里记录已经获取记录数的模块
    #     with open('logtest.txt','a+') as fout:
    #         fout.write('\n*******' + str(datetime.datetime.now()) + '*************')
    #         fout.write( '\n %9.0f records has been stored in MySQL ' %self.total)

    @ToolsBox.mylog
    @ToolsBox.exeTime
    def craw_a_page(self,new_url):
        
        # 计算并打印延时情况 
        if self.delay > 0 :
            sleepSeconds = random.randint(self.delay,self.delay*2)
            print ('craw {0} after {1} seconds ({2} ~ {3}):'.format(
                self.count,sleepSeconds,self.delay,self.delay*2))
        else:
            print ('craw {0} :'.format(self.count))
        
        # 获取请求头、代理信息
        proxy = self.proxy_builder()
        self.headers_builder()

        # 下载
        html_cont = self.downloader.download(new_url,headers=self.headers,
            proxy=proxy,num_retries=self.retry_times)
        
        # 对下载内容进行处理
        # 1、如果被404的处理
        if html_cont == 404:                    
            self.HTTP404 += 1
            time.sleep( 30 * self.HTTP404 )                             #被禁止访问了，消停一会
            if self.HTTP404 > self.HTTP404_stop:
                input('你似乎被禁止访问了，按任意键继续......')
                self.HTTP404 = 0
            else:
                return self.craw_a_page(new_url)
        # 2、正常得到网页
        elif html_cont is not None:
            
            new_urls,new_datas = self.parser.page_parse(html_cont)      #返回解析内容
            
            if new_datas == 'checkcode':                                # 如果解析出是输入验证码
                input("======遇到验证码页面，先保留已解析的数据========")
                self.total = self.total + self.outputer.out_mysql()
                self.outputer.clear_datas()
                self.delay = int(new_urls)               # 调整延时值
                if retries > 0:
                    return self.craw_a_page(new_url,retries - 1)
            
            elif len(new_datas) == 0 and len(new_urls) == 0:            # 解析无数据
                with open('logtest.txt','a+') as fout:
                    fout.write('\n*******' + str(datetime.datetime.now()) + '*************')
                    fout.write( '\n no new datas have been crawed :%s. \n' %new_url)
                print(' There are %s datas and %s urls in %s' %(len(new_datas),len(new_urls),new_url))
                self.nodata += 1                #只有连续5个页面没有数据才会停止
                
                if self.nodata < self.nodata_stop:
                    print("You are still have " + str(self.nodata_stop-self.nodata) + "times to parse this url") 
                    time.sleep(random.randint(3,7))
                    # return self.craw_a_page(new_url,keywords,from_, retries - 1)
                    return self.craw_a_page(new_url,keywords,from_)
            
            # 正常情况，解析
            else:
                # 取页码表
                self.urls.add_new_urls(new_urls)

                # 取小区表，但58的不取了
                # if from_ != '8' :
                #     self.comms.add_new_urls([name['community_name'] for name in new_datas]) 
                # elif keywords == '*':
                #     self.comms.add_new_urls([name['comm_url'] for name in new_datas])
                
                self.comms.add_new_urls([name['community_name'] for name in new_datas]) 

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
                self.HTTP404 = 0          #如果有数据，把self.HTTP404计数器清零
        
        # html_cont内容是None
        else:
            print('craw %s fail : nothing' %(new_url))

        # 延时模块：放在最后，第一次抓取时不用延时
        if self.delay > 0 :
            time.sleep(sleepSeconds)             #2017.5。15把下载延时功能放在这里，这个模块相当于控制器



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


