#coding:utf-8
# import sys

# 学习使用pymysql,以后程序可以升级到python3以上的版本
import pymysql
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
        # sql = 'SELECT * FROM for_sale_propert LIMIT %s,%s'
        sql = 'CREATE TABLE %s LIKE %s'
        newname = "abc"
        cursor.execute(sql %("new_for_sale","for_sale_property"))
        # cursor.execute(sql, ("now_for_sal", "for_sale_property"))
        result = cursor.fetchall()
        # for item in result:
        #     for key,value in item.items():
        #         print('%20s : %s' %(key,value))
        	# print(item)
        # print(result)
    # 如果是创建新表，不用commit也能生效
    # connection.commit()
except Exception as e:
	print(type(e))
	for item in e:
		print(item)
	# 	print(e[0])
	# print(e[1])
finally:
    connection.close();