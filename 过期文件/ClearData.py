#coding:utf-8
import MySQLdb
import  re

def confir(str):
    for i in range(0,32):
        str = str.replace(chr(i),'')
    return  str


db = MySQLdb.connect(host = "192.168.1.207",user = "root",passwd = "root",port = 3306,db = "property_info",charset = "utf8")
cursor = db.cursor()


comm = "联发新天地153号".rstrip()
new_comm = "联发新天地"
select_sql = """SELECT title,community_name,spatial_arrangement,floor_index,total_floor,price,builded_year,area,\
    total_price,advantage,first_acquisition_time,details_url,from_,id FROM for_sale_property_all  WHERE community_name  LIKE '%%%s%%'"""%comm

cursor.execute(select_sql)
datas = cursor.fetchall()
#print (datas)
for d in datas:
  #print type(d[4].encode("utf8"))
  d = list(d)
  #d[1] = new_comm
  d[4] = filter(str.isdigit,str(d[4]).encode("utf8"))
  d[6] = filter(str.isdigit,str(d[6]).encode("utf8"))
  # d[1] = confir(d[1])
  # d[1] = re.split(ur"[-|（| |.|、|,|，|(|。|·|；|《|<]",d[1])[0]
  d[1] = new_comm
  try:
    update_sql = """UPDATE for_sale_property_all SET community_name = %s ,total_floor = %s ,builded_year = %s where id = %s"""
    cursor.execute(update_sql,(d[1],d[4],d[6],d[13]))
    db.commit()
  except MySQLdb.Error,e:
    if e.args[0] == 1062 :
        del_sql = "DELETE from for_sale_property where id = %s"
        cursor.execute(del_sql,d[13])
        db.commit()

  #showlist(d)
  for i in d :
  	print i
  print "-"*35
cursor.close()
db.close()
