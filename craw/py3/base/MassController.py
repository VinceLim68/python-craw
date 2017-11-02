import UrlManager,ToolsBox,Downloader,Outputer,ReqBuilder,WbPage
import time,random,datetime

class MassController(object):
    
    def __init__(self,parseClass):
        
        self.urls = UrlManager.UrlManager()             # url管理
        self.comms = UrlManager.UrlManager()            # 小区管理
        self.downloader = Downloader.Downloader()       # 下载器
        self.parser = parseClass()
        self.outputer = Outputer.Outputer()
        self.rqBuilder = ReqBuilder.ReqBuilder()
        
        self.headers = {}                               #构筑请求头
        self.HTTP404 = 0                                #计数：被404的次数
        self.HTTP404_stop = 3                           #设置：累计404多少次后暂停程序
        self.retry_times = 3                            #设置：下载失败后重试的次数
        self.count = 1                                  #计数：下载页面数
        self.delay = 0                                  #设置：下载页面之间的延时秒数
        self.total = 0                                  #计数：成功加入数据库的记录数量

        self.nodata = 0                                 #计数：连续出现解析不出数据的次数
        self.nodata_stop = 4                             #设置：同一页面如果解析不出数据，可重复次数
        

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
            print(url)
        
        # 2、循环抓取数据
        while self.urls.has_new_url() :
            url = self.urls.get_new_url()
            self.craw_a_page(url)

        # 3、循环结束后，把余下的数据保存起来
        # self.total = self.total + self.outputer.out_mysql()
        
    @ToolsBox.mylog
    @ToolsBox.exeTime
    def craw_a_page(self,new_url,retries = 3):
        
        # 计算并打印延时情况 
        if self.delay > 0 :
            sleepSeconds = random.randint(self.delay,self.delay*2)
            print ('craw {0} after {1} seconds ({2} ~ {3}):'.format(
                self.count,sleepSeconds,self.delay,self.delay*2))
        else:
            print ('craw {0} :'.format(self.count))
        
        # 获取请求头、代理信息,每个页面都不相同
        # proxy = self.proxy_builder()
        proxy = None
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
                self.delay = input("遇到验证码，输入延时秒数后，保留已解析的数据......")
                if self.delay == '':
                    self.delay = 0
                else:
                    self.delay = ToolsBox.strToInt(self.delay)
                self.total = self.total + self.outputer.out_mysql()
                if retries > 0:
                    return self.craw_a_page(new_url,retries - 1)
            elif len(new_datas) == 0 and len(new_urls) == 0:            # 解析无数据
                self.nodata += 1                
                if self.nodata < self.nodata_stop:
                    print("本页面未解析出数据，可再试{0}次".format(self.nodata_stop-self.nodata))
                    time.sleep(random.randint(3,7))
                    return self.craw_a_page(new_url)
                else:
                    with open('logtest.txt','a+') as fout:
                        fout.write('\n*******' + str(datetime.datetime.now()) + '*************')
                        fout.write('\n 本页面无数据:%s. \n' %new_url)
            else:                                                        # 正常情况，解析
                print('本页面      datas:{0}，urls:{1}'.format(len(new_datas),len(new_urls)))
                # 把页面链接放入url管理器
                self.urls.add_new_urls(new_urls)
                # 把小区名称放入小区管理器
                for data in new_datas:
                    self.add_comm(data)
                    # if len(data['community_name']) > 11 :
                    #     print('{0}---->名字过长的小区名将被忽略。'.format(data['community_name']))
                    # else:
                    #     comm = self.comms.add_new_url(data['community_name'])
                    #     if comm:
                    #         print('>>>>>>>>>>>>>>>>{0}'.format(comm))
                # 把挂牌信息传入outputer，清除无效数据后，放在outputer.raw_datas记录集中
                self.outputer.collect_data(new_datas)
                data_num = self.outputer.get_datas_quantity()
                print("共%6.0f = %6.0f 重复 + %5.0f 数据池 + %6.0f 存入数据库 "
                      % (data_num['dupli_count'] + data_num['r_data'] + self.total,
                         data_num['dupli_count'],data_num['r_data'], self.total))

                if 3000 < data_num['r_data']:
                    print("正在存入数据库中，请稍侯......")
                    storenum = self.outputer.out_mysql()
                    if storenum:
                        self.total = self.total + storenum
                self.count += 1
                self.nodata = 0                         #如果有数据，把self.nodata计数器清零
                self.HTTP404 = 0                        #如果有数据，把self.HTTP404计数器清零
        # 3、html_cont内容是None，这是出现500以上的download失败
        else:
            print('未能从服务器上下载{0}'.format(new_url))

        # 延时模块：放在最后，第一次抓取时不用延时
        if self.delay > 0 :
            time.sleep(sleepSeconds)             #2017.5。15把下载延时功能放在这里，这个模块相当于控制器

    def add_comm(self,data):
        #把添加小区列表提出来，因为会有不一样的需求，有的需要小区名称，有的需要小区链接
        comm_add = data['community_name']
        if len(comm_add) > 11:
            print('{0}---->名字过长的小区名将被忽略。'.format(comm_add))
        else:
            comm = self.comms.add_new_url(comm_add)
            if comm:
                print('>>>>>>>>>>>>>>>>{0}'.format(comm))

if __name__=="__main__":
    url = ['http://xm.58.com/ershoufang/pn2/']
    MC = MassController(WbPage.WbPage)
    MC.craw_controller(url)

    # if from_where == 1:
    #     root_url = ['http://xm.anjuke.com/sale/p1-rd1/?kw=' + serch_for + '&from_url=kw_final#filtersort']
    #     obj_spider = SpiderMain(AJK_parser.AjkParser())
    # if from_where == 2:
    #     root_url = ['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_1.html'] if keywords == '*' \
    #             else ['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s1_itp_b0_it_if_ih1_p-_ar-_pt_o0_ps20_1.html?keyWord=' + serch_for ]
    #     obj_spider = SpiderMain(XM_parser.XmParser())
    # if from_where == 3:
    #     root_url = ['http://esf.xm.fang.com/house/c61-kw' + urllib.quote(unicode(keywords,"utf-8").encode('gbk')) +'/']
    #     obj_spider = SpiderMain(SF_parser.SfParser())
    # if from_where == 4:
    #     root_url = ['http://xiamen.qfang.com/sale/f1','http://xiamen.qfang.com/sale/f2'] if keywords == '*' \
    #             else ["http://xiamen.qfang.com/sale/f1?keyword=" + serch_for,"http://xiamen.qfang.com/sale/f2?keyword=" + serch_for]
    #     obj_spider = SpiderMain(QF_parser.QfParser())
    # if from_where == 5:
    #     root_url = ['http://xm.lianjia.com/ershoufang/pg1/'] if keywords == '*' \
    #             else ["http://xm.lianjia.com/ershoufang/rs" + serch_for]
    #     obj_spider = SpiderMain(LJ_parser.LjParser())
    # if from_where == 6:
    #     root_url = ['http://xm.ganji.com/fang5/o1/'] 
    #     obj_spider = SpiderMain(LJ_parser.LjParser())

    # obj_spider.craw(root_url,keywords,from_where)
    # obj_spider.out(from_where)


