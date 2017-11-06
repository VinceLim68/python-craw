# coding:utf-8
import sys
import MySQLdb
import MySQLdb.cursors
reload(sys)
sys.setdefaultencoding("utf-8")
# import xlrd

class MatchID(object):
    """
    将挂牌信息中的小区名称匹配成相应的小区id的对象
    """

    def __init__(self):
        self.db = MySQLdb.connect(
            host = "192.168.1.207",user = "root",passwd = "root",
            port = 3306,db = "property_info",charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def get_comm_arr_fromMysql(self,pri):
        # 从comm表，生成comm数组
        # 按关键字进行了拆分，一个id会有多个关键字
        # 返回：每个comm_arr按[id,小区关键字]  
        where = "where pri_level=" + str(pri)
        sql = "SELECT comm_name,comm_id,keywords,pri_level FROM comm " + where
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        comm_arr = []
        for data in datas:
            comms = data['keywords'].split(',')     #data[2] = keywords,把keywords用“,”进行拆分
            for comm in comms:
                kv = []
                kv.append(data['comm_id'])
                kv.append(comm)
                comm_arr.append(kv)     
        return comm_arr

    def get_id_from_arr(self,data,comm_arr):
        # 传入一条挂牌记录(list)，匹配出与小区id相关的数组
        # 都是在小区名里寻找是否能匹配到关键字

        # 取出小区名称,data[11]=comm_name
        commName = data['community_name'].replace("·","").replace(".","").encode("utf8").upper()

        getid = []              # getid:[开始位置，关键字，id]   
        
        # 轮询小区id与其关键字的对应数组
        for i in comm_arr:                              
            # i[1]=keywords ，关键字后带辅助字的，先将关键字与辅助字拆开
            key_words = i[1].split("/")                 
            
            # 在小区名称中查找关键字，不含辅助字
            start = commName.find(key_words[0].upper())         
            
            # 如果找到
            if start >= 0:
                # 如果有带辅助字，必须同时匹配到辅助字才可以
                lenth = len(key_words)
                if lenth > 1:               
                    if data['title']:
                    # try:
                        #把title+community_name相加成一个供匹配字段
                        formatch = commName + data['title'].encode("utf8").upper() 
                    else:
                        formatch = commName
                    # except:
                    #     print('??????????%s'%(data['id']))


                    
                    # 在formatch中查找辅助字
                    for j in range(1,lenth):
                        # 只要找到一个，说明符合条件，即可退出循环
                        if formatch.find(key_words[j].upper()) >=0:     
                            temp = [start,key_words[0].upper(),i[0]]    #key_words[0] = keyword , key_words[1]以后的是辅助字
                            getid.append(temp)                          #i[0]就是comm_id
                            break
                # 如果没有辅助字
                else:
                    temp = [start,key_words[0].upper(),i[0]]            
                    getid.append(temp)
        
        # 返回：[起始位置，关键字，id]
        return getid

    def get_datas(self,n,step):
        #从数据库里按要求查出挂牌记录集        
        sql = "SELECT id,title,community_name FROM for_sale_property WHERE community_id is NULL or community_id = 0 ORDER BY id LIMIT " + str(n) + "," + str(step)
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        return datas

    def update_id(self,dataid,comm_id):
        # 把匹配成功的commid写入表中
        sql_update = "UPDATE for_sale_property SET community_id = %s WHERE id = %s"
        # sql_update = "UPDATE for_sale_property SET community_id = comm_id WHERE id = dataid"
        print(dataid)
        self.cursor.execute(sql_update,(comm_id,dataid))
        self.db.commit()

    
    def insert_err(self,data):
        print("---------nofind---------")
        # print(data,'nofind****************')
        for key,value in data.items():
            print('%20s : %s' %(key,value))

    def insert_mul(self,data,get):
        # 对匹配到多个id的,而且解析不出来的，转存到for_sale_mul中去，以备人工复核
        sql_update = "UPDATE for_sale_property SET community_id = %s WHERE id = %s"
        self.cursor.execute(sql_update,(len(get),data['id']))
        self.db.commit()
        print("%s---------mul"%(data['id']))
        return

    def insert_mul_for_check(self,data,getid,comm_id):
        #这是把所有匹配到多个id的记录都存到表for_sale_mul_check，主要是调试用的,该表会过滤重复的多匹配字段
        get1 = ""
        f1 = False
        a = getid[0][2]                 #getid[0][2] = comm_id
        for item in getid:
            if item[2] != a:            #如果虽然匹配成功多个小区关键字，可是小区id是一样的，忽略
                f1 = True
            get1 += str(item[0]) + "," + item[1] + "," + str(item[2]) + "|"

        if f1:
            try:
                print(str(k)+"---------mul----for checked")
                print(get1)
                sql_insert ="INSERT for_sale_mul_check (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
                                details_url,community_name,first_acquisition_time,from_,getid,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],\
                    data[9],data[10],data[11],data[12],data[13],get1,comm_id))
                self.db.commit()
            except MySQLdb.Error as e:
                pass

    def handle_match_mul(self,data,getid):
        """
        处理 getid 中匹配成功不止一个id
        处理的原则是以起始字段在前的为准，
        如果超始字段相同，则以字符串长的为准
        如果起始与字串长度都一样，则人工判断
        """
        flag = False                            #标志位，如果能解析出唯一id,则标志位设成ture
        
        getid.sort(key=lambda x:x[0])           #按照匹配关键字的起始位置排序     
        
        #起始位置最小的getid
        first = getid[0]
        
        # 用第一个匹配成的合成一个字段：起始位置+小区名称+小区id
        # get = str(getid[0][0]) +',' + str(getid[0][1]) +',' + str(getid[0][2]) + "/"      
        # 传进getid,挑选出get
        get = getid[0]
        
        for l in range(1,len(getid)):
            # 如果第二个匹配到的关键字起始位置大于第一个，就以第一个为准，不用再匹配了
            if(getid[l][0] > first[0]):         
                break
            else:                               #如果有并列第一：
                if len(getid[l][1]) > len(first[1]):        #字符串长的优先
                    first = getid[l]
                elif len(getid[l][1]) == len(first[1]):     #字符串长度相同的，标志位设成ture,要人工判断一下
                    # 起始位置相同，关键字长度相同，不知道是哪个小区了
                    get.append(getid[l])
                    # get += str(getid[l][0]) +',' + str(getid[l][1]) +',' + str(getid[l][2]) + "/"
                    flag = True
        # 匹配成功写入一张表，没成功就写入另一张表。
        # 其实不用，成功就写进id,没成功就空着即可
        if flag:
            self.insert_mul(data,get)
        else:
            self.update_id(data['id'],first[2])

        # self.insert_mul_for_check(data,getid,first[2])


    def close_db(self):
        self.cursor.close()
        self.db.close()


if __name__=="__main__":
    n = 0
    step = 100000
    k = 0
    dupli = 1

    matchid = MatchID()

    comm_arr = matchid.get_comm_arr_fromMysql(0)
    road_arr = matchid.get_comm_arr_fromMysql(1)
    
    datas = matchid.get_datas(n,step)

    for data in datas:
        getid = matchid.get_id_from_arr(data,comm_arr)
        try:
            if len(getid) == 1:                                     #如果匹配到唯一id
                matchid.update_id(data['id'],getid[0][2])
            elif len(getid) == 0:                                   #如果没匹配到comm，就看看按road是否能匹配
                getroad = matchid.get_id_from_arr(data,road_arr)
                if len(getroad) == 1:                               #匹配到唯一road                              
                    matchid.update_id(data['id'],getroad[0][2])
                elif len(getroad) == 0: 
                    # pass                          #如果连road也没匹配成功，空在那里
                    matchid.insert_err(data)
                elif len(getroad) > 1:                              #如果匹配到不止一个road,进行处理
                    matchid.handle_match_mul(data,getroad)
            elif len(getid) > 1:                                    #如果comm匹配到不止一个，进行处理
                matchid.handle_match_mul(data,getid)
                
        
            k = k + 1

        except MySQLdb.Error,e:
            if e.args[0] == 1062 :
                print(str(dupli)+"aready have")
                dupli = dupli + 1

    matchid.close_db()