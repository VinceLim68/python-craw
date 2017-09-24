
# s = input('看看中文可能吗:')
# print(type(s*5))
# print('直接输出中文')
# 结论：可以直接输出中文不用解码

# =============================================
# import pymysql
#
# try:
#     conn=pymysql.connect(host = "192.168.1.207",user = "root",passwd = "root",db = "property_info",charset = "utf8")
# except:
#     print( "Connect failed")
#
# cur = conn.cursor(cursor=pymysql.cursors.DictCursor)            # 用字典
#
# cur.execute("SELECT VERSION()")
# data = cur.fetchone()
# print ("Database version : %s " % data)
#
# sql = 'select * from for_sale_property limit 1,5'
# cur.execute(sql)
# # print(cur.rowcount)
# data = cur.fetchall()
# for d in data:
#     print('-'*50)
#     print(d )
#     for key in d:
#         print('%20s : %s' %(key,d[key]))

import pymysql