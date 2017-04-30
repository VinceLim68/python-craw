#coding:utf-8
import MySQLdb
import re
import urllib
import traceback 
import datetime

def confir(str):
    for i in range(0,32):
        str = str.replace(chr(i),'')
    return  str


db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS for_sale_property_bak")
create_table_sql = """CREATE TABLE for_sale_property_bak (
    id int(10) unsigned NOT NULL AUTO_INCREMENT,
    title varchar(150) DEFAULT NULL,
    community_id int(7) unsigned,
    community_name varchar(50) NOT NULL,
    spatial_arrangement varchar(20) DEFAULT NULL,
    floor_index tinyint(3) DEFAULT 0,
    total_floor tinyint(3) unsigned,
    price float(10,2) unsigned NOT NULL,
    builded_year int(4) unsigned,
    area float(11,2) unsigned NOT NULL,
    total_price float(11,2) unsigned NOT NULL,
    advantage varchar(20) DEFAULT NULL,
    first_acquisition_time date DEFAULT NULL,
    details_url varchar(150) NOT NULL,
    from_ varchar(10) DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY `summary_index` (`community_name`,`floor_index`,`area`,`total_price`) USING HASH,
    KEY `c_name` (`community_name`) USING BTREE)"""

# cursor.execute("DROP TABLE IF EXISTS invalid_property")
# create_invalid_property_sql = """CREATE TABLE invalid_property (
#     id int(10) unsigned NOT NULL AUTO_INCREMENT,
#     title varchar(150) DEFAULT NULL,
#     community_id int(7) unsigned,
#     community_name varchar(50) NOT NULL,
#     spatial_arrangement varchar(20) DEFAULT NULL,
#     floor_index tinyint(3) DEFAULT 0,
#     total_floor tinyint(3) unsigned,
#     price float(10,2) unsigned NOT NULL,
#     builded_year int(4) unsigned,
#     area float(11,2) unsigned NOT NULL,
#     total_price float(11,2) unsigned NOT NULL,
#     advantage varchar(20) DEFAULT NULL,
#     first_acquisition_time date DEFAULT NULL,
#     details_url varchar(150) NOT NULL,
#     from_ varchar(10) DEFAULT NULL,
#     PRIMARY KEY (id),
#     UNIQUE KEY `summary_index` (`community_name`,`floor_index`,`area`,`total_price`) USING HASH,
#     KEY `c_name` (`community_name`) USING BTREE)"""

# cursor.execute(create_invalid_property_sql)
cursor.execute(create_table_sql)
count = 1
dupli = 0

count_sql = "select count(id) from for_sale_property"
cursor.execute(count_sql)
datas = cursor.fetchall()
all_num = datas[0][0]

select_sql = """SELECT title,community_name,spatial_arrangement,floor_index,total_floor,price,builded_year,area,\
    total_price,advantage,first_acquisition_time,details_url,from_,id FROM for_sale_property  WHERE id >= %s and id < %s + 2000  """
ins_sql = "INSERT for_sale_property_bak (title,community_name,spatial_arrangement,floor_index,total_floor,price,builded_year,area,\
            total_price,advantage,first_acquisition_time,details_url,from_)\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
records = 0
while records <= all_num + 2000:
    cursor.execute(select_sql,(count,count))
    datas = cursor.fetchall()

    for d in datas:
              
        d = list(d)
        d[4] = filter(str.isdigit,str(d[4]).encode("utf8"))
        d[6] = filter(str.isdigit,str(d[6]).encode("utf8"))
        d[1] = confir(d[1])
        d[1] = re.split(ur"[-|（| |、|,|，|(|。|；|《|<]",d[1])[0]
        try:
            records += 1
            cursor.execute(ins_sql,(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],d[12]))
            db.commit()
            print "========= %s valid "%records
        except MySQLdb.Error,e:
            with open('copylog.txt','a+') as fout:
                if e.args[0] == 1062 :
                    # for i in d:
                    #     print i
                    dupli += 1
                    print "Find %s duplicate datas"%dupli
                fout.write(str(datetime.datetime.now()) + '\n')
                traceback.print_exc(file=fout) 
                traceback.print_exc()

    count = count + 2000

cursor.close()
db.close()
