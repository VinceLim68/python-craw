import pymysql
conn = pymysql.connect(host="office.xmcdhpg.cn", user="root", passwd="root", db="property_info", charset="utf8",port = 3306)
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)