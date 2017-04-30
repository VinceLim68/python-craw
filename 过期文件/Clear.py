#coding:utf-8
import MySQLdb
# import re
from random import choice
import urllib
import traceback 
import datetime
import time
import random

def confir(str):
    for i in range(0,32):
        str = str.replace(chr(i),'')
    return  str


db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
cursor = db.cursor()

count = 121
dupli = 0

count_sql = "select count(id) from for_sale_property"
cursor.execute(count_sql)
datas = cursor.fetchall()
all_num = datas[0][0]

select_sql = """SELECT title,community_name,spatial_arrangement,floor_index,total_floor,price,builded_year,area,\
    total_price,advantage,first_acquisition_time,details_url,from_,id FROM for_sale_property  WHERE id >= %s and id < %s + 2000  """

ins_sql_invalid = "INSERT invalid_property (title,community_name,spatial_arrangement,floor_index,total_floor,price,builded_year,area,\
            total_price,advantage,first_acquisition_time,details_url,from_)\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
records = 0
print " start ....."
# while records <= all_num + 2000:
while records <= all_num + 2000:
    cursor.execute(select_sql,(count,count))
    datas = cursor.fetchall()

    for d in datas:
        # print d[11]
        records += 1
        try:
            status = urllib.urlopen(d[11]).code

            print "the status is %s"%status
            if status == 404 :
                # try:
                cursor.execute(ins_sql_invalid,(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],d[12]))
                print "insert ok,the id is %s"%d[13]
                cursor.execute("DELETE FROM for_sale_property WHERE id = %s"%d[13])
                print "dele ok"
                db.commit()
                print "========= %s invalid "%records
            else:
                print d[11]
                time.sleep(random.randint(5,7))
        except:
            with open('copylog.txt','a+') as fout:
                fout.write(str(datetime.datetime.now()) + '\n')
                traceback.print_exc(file=fout) 
                traceback.print_exc()

    count = count + 2000

cursor.close()
db.close()
