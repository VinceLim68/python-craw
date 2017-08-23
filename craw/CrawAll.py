#coding:utf-8
#这是持续抓取挂牌记录的程序,修改为继承house类
from spider import url_manager,html_downloader,AJK_parser,html_outputer,SF_parser,LEJU_parser,LJ_parser,XM_parser,mytools,MT_parser,GJ_parser,WB_parser
from house4 import SpiderMain
import urllib
import time,random
import traceback  
import sys
import datetime


class SpiderAll(SpiderMain):
    def __init__(self,parseClass):
        SpiderMain.__init__(self,parseClass)
        self.count1 = 1

    def craw_control(self,from_where):
        self.quantity_of_new_comms = 1
        while self.quantity_of_new_comms:
            self.craw_one_comm(from_where)
        self.total = self.total + self.outputer.out_mysql()
        self.print_record()
        self.outputer.clear_datas()

    
    # @mytools.mylog
    def craw_one_comm(self,from_where):
        
        # 从小区列表中取一个小区出来
        try:
            new_comm = self.comms.get_new_url().encode("utf8")
        except Exception, e:
            print(traceback.format_exc())
            print('debug : no new_comm')
            return

        # 小区列表中还有多少未抓小区，多少已抓小区
        self.quantity_of_new_comms,quantity_of_old_comms = self.comms.get_quantity()
        try:
            print "********** %s :Crawing %s **************"%(self.count1,unicode(new_comm,"utf-8").encode("gbk"))
        except:
            print "********** %s :Crawing **************"%(self.count1)
        
        print " Communities : %5.0f / %5.0f " \
                    %(quantity_of_old_comms,self.quantity_of_new_comms + quantity_of_old_comms)
        
        
        # URL 编码
        # 生成小区的查询url
        serch_for = urllib.quote(new_comm)
        if from_where == '1':
            search_url = ['http://xm.anjuke.com/sale/p1-rd1/?kw=' + serch_for + '&from_url=kw_final#filtersort']
        if from_where == '3':
            search_url = ['http://esf.xm.fang.com/house/c61-kw' + urllib.quote(unicode(new_comm,"utf-8").encode('gbk')) +'/']
        # if from_where == '6':
        #     search_url = ["http://xm.maitian.cn/esfall/RS" + serch_for]
        if from_where == '5':
            search_url = ["http://xm.lianjia.com/ershoufang/rs" + serch_for]
        if from_where == '8':
            # search_url = [new_comm]
            search_url = ["http://xm.58.com/ershoufang/?key=" + new_comm + "&sourcetype=5"]

        # print(search_url)
        # 按小区抓取数据
        self.craw(search_url,new_comm,from_where)
        self.count1 = self.count1 + 1

       

if __name__=="__main__":

    if len(sys.argv) < 2:
        print('The argvs are needed here,1-anjuke,2-xmhouse,3-fang,4-qfan,5-lianjia')

    for i in sys.argv:
        from_where = i
        if from_where == '1':
            root_url = ["http://xm.anjuke.com/sale/p1/#filtersort"]
            obj_spider = SpiderAll(AJK_parser.AjkParser())
        if from_where == '2':
            root_url = ['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html'] 
            obj_spider = SpiderMain(XM_parser.XmParser())
        if from_where == '3':
            root_url = ["http://esf.xm.fang.com/"]
            obj_spider = SpiderAll(SF_parser.SfParser())
        if from_where == '4':
            root_url = ['http://xm.esf.leju.com/house/n200'] 
            obj_spider = SpiderMain(LEJU_parser.LejuParser())
            # pass
            # Q房网好象取消提供厦门的房产信息
            # root_url = ['http://xiamen.qfang.com/sale/f1','http://xiamen.qfang.com/sale/f2']
            # obj_spider = SpiderAll(QF_parser.QfParser())
        if from_where == '5':
            root_url = ['http://xm.lianjia.com/ershoufang/pg1/']
            obj_spider = SpiderAll(LJ_parser.LjParser())
            # obj_spider = SpiderMain(LJ_parser.LjParser())
        if from_where == '6':
            root_url = ['http://xm.maitian.cn/esfall/PG2']
            # obj_spider = SpiderAll(MT_parser.MTParser())
            obj_spider = SpiderMain(MT_parser.MTParser())
        if from_where == '7':
            root_url = ['http://xm.ganji.com/fang5/o2/']
            obj_spider = SpiderMain(GJ_parser.GjParser())
        if from_where == '8':
            root_url = ['http://xm.58.com/ershoufang/pn1/']
            obj_spider = SpiderAll(WB_parser.WBParser())

        if from_where != 'crawall.py':
            obj_spider.craw(root_url,"*",from_where)                        #爬取第一批网页
            # print('-'*50)
            # raw_input('debug:================')
            if from_where == '1' or from_where == '3'  or from_where == '8' or from_where == '5':
                obj_spider.craw_control(from_where)
            else:                                     #2016.8.15 对于2(厦门联合网)、4（Q房网),5(链家）一次抓取完成,退出时要把剩余的数据存储一下
                obj_spider.outputer.out_mysql()
                obj_spider.outputer.clear_datas()                           


    



