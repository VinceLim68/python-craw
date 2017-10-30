import bloomfilter
import ToolsBox
import pymysql
import datetime
import traceback

class Outputer(object):
    # 数据后处理器
    __instance = None

    def __init__(self):
        # reload(sys)
        # sys.setdefaultencoding("utf-8")
        # self.datas = []                       #数据集：挑选出的数据（根据小区名称挑选），但如果只是抓取数据不需要
        self.raw_datas = []                     #数据集：原始数据
        self.dupli_count = 0                    #计数：重复的数据
        self.now = datetime.date.today()        #字段：插入记录的日期

        self.key_infos = bloomfilter.BloomFilter(0.001,1000000)     #学习使用bloomfilter

        try:
            # self.conn=pymysql.connect(host = "192.168.1.207",user = "root",passwd = "root",db = "property_info",charset = "utf8")
            self.conn=pymysql.connect(host = "office.xmcdhpg.cn",user = "root",passwd = "root",db = "property_info",charset = "utf8",port = 3306)
        except:
            print( "Connect failed")
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)            # 用字典


    # 单例。
    def __new__(cls,*args,**kwd):
        if Outputer.__instance is None:
            Outputer.__instance = object.__new__(cls,*args,**kwd)
        return Outputer.__instance



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
            except pymysql.err.IntegrityError as e:
            # except MySQLError as e:
                if e.args[0] == 1062 :
                    dupli = dupli + 1
                else:
                    with open('logtest.txt','a+') as fout:      #2017.3把错误日志改成logtest.txt
                        fout.write(str(datetime.datetime.now()) + 'record by outputer \n')
                        traceback.print_exc(file=fout)
                    print(traceback.format_exc())
                        # traceback.print_exc()
                    # print(MySQLError,":",e)
                    code, message = e.args
                    print(code,message)
            except pymysql.err.InterfaceError as e:
                # 有的时候长时间暂停，connect会断开，要重新连接一下
                try:
                    self.conn = pymysql.connect(host="192.168.1.207", user="root", passwd="root", db="property_info",
                                                charset="utf8")
                except:
                    print("Connect failed")
                self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


        # cursor.close()
        # db.close()
        print("本次共{0}个数据，存入{1},重复{2}".format(len(self.raw_datas),success,dupli))
        self.dupli_count += dupli
        self.clear_datas()
        return success

    # def get_datas(self):
    #     return self.datas

    def get_datas_quantity(self):
        data_num = {}
        data_num['r_data'] = len(self.raw_datas)                #计数：有效数据数量
        data_num['dupli_count'] = self.dupli_count              #计数：重复数据
        return data_num

    def clear_datas(self):
        # self.datas = []             #清洗后的数据
        self.raw_datas = []         #原始数据
        return

    def close_db(self):
        self.cur.close()
        self.conn.close()
        return