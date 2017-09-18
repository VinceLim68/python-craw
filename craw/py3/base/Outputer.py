#coding:utf-8
# import sys
# import xlsxwriter
# import myStat
import bloomfilter
import ToolsBox
import pyMySql
import datetime
import traceback

class Outputer(object):
    # 数据后处理器

    def __init__(self):
        # reload(sys)
        # sys.setdefaultencoding("utf-8")
        # self.datas = []                       #数据集：挑选出的数据（根据小区名称挑选），但如果只是抓取数据不需要
        self.raw_datas = []                     #数据集：原始数据
        self.dupli_count = 0                    #计数：重复的数据
        self.now = datetime.date.today()        #字段：插入记录的日期
        
        self.key_infos = bloomfilter.BloomFilter(0.001,1000000)     #学习使用bloomfilter

        try:
            self.conn=pymysql.connect(host = "192.168.1.207",user = "root",passwd = "root",db = "property_info",charset = "utf8")      
        except:
            print( "Connect failed")
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)            # 用字典


    # 单例
    def __new__(cls,*args,**kwd):
        if Outputer.__instance is None:
            Outputer.__instance = object.__new__(cls,*args,**kwd)
        return Outputer.__instance

    
    def pipe(self,datadic):
        # 清理无效数据
        if datadic.has_key('total_floor') and datadic.has_key('total_price') and datadic.has_key('area') and datadic.has_key('community_name'):
            if datadic['community_name'] is None or len(datadic['community_name'])<=2:return False
            datadic['community_name'] = datadic['community_name'].strip()
            
            if datadic['total_price'] is None or datadic['area'] is None :return False
            if datadic['total_floor'] > 60: datadic['total_floor'] = 35         #把过高楼层的设为35层
            if datadic['total_price'] == 0 : return False                       #2016.9.13 价格为0的过滤掉
            
            if datadic.has_key('builded_year'):
                if datadic['builded_year'] < 1900: datadic['builded_year'] = 0
            
            if datadic['area'] > 20000: return False                            #面积过大，有时是填写错误，而且面积大于20000的价格参考意义也不大，舍弃
            if not datadic.has_key('price'): return False                       #2016.8.1 有时解析过程中出错，跳过了price字段解析，造成没有price,舍弃
            
            # detail_url字段太长，处理一下
            if len(datadic['details_url']) > 250:datadic['details_url'] = datadic['details_url'][:249]
            
            if len(datadic['advantage']) > 20:datadic['advantage'] = datadic['advantage'][:20]
            return datadic
        else:
            if not datadic.has_key('total_floor'):                    #2016.6.1搜房网老是出现无效数据，进行判断，发现是别墅没有记载楼层信息造成的
                if u"别墅" in datadic['title']:
                    datadic['total_floor'] = 4
                    datadic['floor_index'] = 1
                    datadic['spatial_arrangement'] = datadic['spatial_arrangement'] + u"别墅"
                    return datadic
            return False

    def collect_data(self,datas):
        # 清理重复数据
        if datas is None or len(datas) == 0:
            return
        for onedata in datas:
            key_info = str(onedata['area']) + ":" + str(onedata['floor_index']) + ":" + str(onedata['total_price']) + ":" + onedata['community_name']      #用"面积+层次+总价+小区名称"作为关键字来去重

            if not self.key_infos.is_element_exist(key_info):       #2016.5.27用bloomfilter来代替set()
                self.key_infos.insert_element(key_info)
                self.raw_datas.append(onedata)
            else:
                self.dupli_count += 1


    
    @ToolsBox.mylog
    def out_mysql(self):
        dupli = 0       #计数：插入数据库时的重复记录值
        success = 0     #计数：插入数据库的成功记录数量 
        
        sql = """
            INSERT for_sale_property (title,area,spatial_arrangement,price,floor_index,
            total_floor,builded_year,advantage,total_price,details_url,community_name,
            first_acquisition_time,from_) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        for data in self.raw_datas:
            try:
                self.cur.execute(sql,(data['title'],data['area'],data['spatial_arrangement'],data['price'],
                    data['floor_index'],data['total_floor'],data['builded_year'],data['advantage'],data['total_price'],
                    data['details_url'],data['community_name'],self.now,data['from']))
                success = success + 1
                self.conn.commit()
            except MySQLError as e:
                if e.args[0] == 1062 :
                    dupli = dupli + 1
                else:
                    with open('logtest.txt','a+') as fout:      #2017.3把错误日志改成logtest.txt
                        fout.write(str(datetime.datetime.now()) + 'record by outputer \n')
                        traceback.print_exc(file=fout)
                    print(traceback.format_exc())
                        # traceback.print_exc()
                    print(MySQLError,":",e)

        # cursor.close()
        # db.close()
        print("本次共{0}个数据，存入{1},重复{2}".format(len(self.raw_datas),success,dupli))
        self.clear_datas()
        return success

    # def get_datas(self):
    #     return self.datas

    def get_datas_quantity(self):
        data_num = []
        data_num['r_data'] = len(self.raw_datas)                #计数：有效数据数量
        data_num['dupli_count'] = self.dupli_count              #计数：重复数据
        return data_num

    def clear_datas(self):
        # self.datas = []             #清洗后的数据
        self.raw_datas = []         #原始数据
        return