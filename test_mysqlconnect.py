#coding:utf-8
# import sys

# 学习使用pymysql,以后程序可以升级到python3以上的版本
import pymysql
import datetime
config = {
          'host':'localhost',
          'port':3306,
          'user':'root',
          'password':'root',
          'db':'property_info',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }
connection = pymysql.connect(**config)
try:
    with connection.cursor() as cursor:
        getdatas = 'SELECT * FROM for_sale_property LIMIT %s,%s'
        cursor.execute(getdatas %(1600000,10))
        setdatas = "INSERT new_for_sale (title,area,spatial_arrangement,price,floor_index,total_floor,builded_year,advantage,total_price,details_url,community_name,first_acquisition_time,from_) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # sql = 'CREATE TABLE %s LIKE %s'
        # cursor.execute(sql %("new_for_sale","for_sale_property"))
        result = cursor.fetchall()
        for data in result:
            cursor.execute(setdatas,(data['title'],data['area'],data['spatial_arrangement'],data['price'],
                    data['floor_index'],data['total_floor'],data['builded_year'],data['advantage'],data['total_price'],
                    data['details_url'],data['community_name'],datetime.date.today(),data['from_']))
            # for key,value in data.items():
            #     print('%20s : %s' %(key,value))
            # print(data['title'])
            # print(data['from_'])
    # 如果是创建新表，不用commit也能生效
    connection.commit()
except Exception as e:
	print(type(e))
	for item in e:
		print(item)
finally:
    connection.close();