#coding:utf-8
import sys
import xlsxwriter
# import myStat
import bloomfilter
import mytools
import MySQLdb
import datetime
import traceback

class HtmlOutputer():
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.datas = []             #清洗后的数据
        self.raw_datas = []         #原始数据
        
        # self.key_infos = set()      #帮助去除重复数据
        self.key_infos = bloomfilter.BloomFilter(0.001,1000000)     #学习使用bloomfilter
        
        self.dupli_count = 0

    def collect_data(self,datas,keywords):
        #主要用于清理数据
        if datas is None or len(datas) == 0:
            return
        for onedata in datas:
            key_info = str(onedata['area']) + ":" + str(onedata['floor_index']) + ":" + str(onedata['total_price']) + ":" + onedata['community_name']      #用"面积+层次+总价+小区名称"作为关键字来去重

            if not self.key_infos.is_element_exist(key_info):       #2016.5.27用bloomfilter来代替set()
                self.key_infos.insert_element(key_info)
                # if key_info not in self.key_infos:
                #     # 先得到原始数据(符合搜索条件，但不一定是本小区的)
                #     self.key_infos.add(key_info)
                
                self.raw_datas.append(onedata)

                if keywords == "*":
                    self.datas.append(onedata)
                elif keywords in onedata['community_name']:
                    self.datas.append(onedata)
            else:
                self.dupli_count += 1


    
    @mytools.mylog
    def out_mysql(self):
        dupli = 0       #计算重复并不被数据库接受的记录数量
        success = 0     #插入成功的记录数量 
        now = datetime.date.today()
        try:
             db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
        except:
            print "Connect failed"
            return self.out_mysql()
        cursor = db.cursor()
        
        sql = "INSERT for_sale_property (title,area,spatial_arrangement,price,\
                floor_index,total_floor,builded_year,advantage,total_price,details_url,community_name,first_acquisition_time,from_)\
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for data in self.raw_datas:
            try:
                cursor.execute(sql,(data['title'],data['area'],data['spatial_arrangement'],data['price'],
                    data['floor_index'],data['total_floor'],data['builded_year'],data['advantage'],data['total_price'],
                    data['details_url'],data['community_name'],now,data['from']))
                success = success + 1
                db.commit()
            except MySQLdb.Error,e:
                if e.args[0] == 1062 :
                    dupli = dupli + 1
                else:
                    with open('logtest.txt','a+') as fout:      #2017.3把错误日志改成logtest.txt
                        fout.write(str(datetime.datetime.now()) + 'record by program \n')
                        fout.write('%s : %s \n floor_index: %s\n total_floor: %s\n community_name: %s\n details_url: %s\n' %(MySQLdb.Error,e,data['floor_index'],data['total_floor'],data['community_name'],data['details_url']))
                        traceback.print_exc(file=fout)
                        print traceback.format_exc()
                        traceback.print_exc()
                    print(MySQLdb.Error,":",e)
                    print('floor_index: %s' %(data['floor_index']))
                    print('total_floor: %s' %(data['total_floor']))
                    print('community_name: %s' %(data['community_name']))
                    print('details_url: %s' %(data['details_url']))
        cursor.close()
        db.close()
        print("Records totally: " + str(len(self.raw_datas)) )
        print(" Stored in MySQL: " + str(success))
        if dupli > 0 :
            print("Duplication: " + str(dupli) )
        return success

    def get_datas(self):
        return self.datas

    def get_datas_quantity(self):
        return len(self.datas),len(self.raw_datas),self.dupli_count

    def clear_datas(self):
        self.datas = []             #清洗后的数据
        self.raw_datas = []         #原始数据
        return