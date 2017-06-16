# coding:utf-8
from match_id_by_mysql import MatchID
import MySQLdb
import xlrd

class MatchIdFromErr(MatchID):
	"""docstring for MatchIdFromErr"""
	# def __init__(self, arg):
	# 	super(MatchIdFromErr, self).__init__()
	# 	self.arg = arg
		
	def get_datas(self):
		#从数据库里按要求查出挂牌记录集		
		sql = "SELECT for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_ FROM for_sale_err"
		self.cursor.execute(sql)
		datas = self.cursor.fetchall()
		return datas

	def insert_for_sale(self,data,comm_id):
		# 把匹配成功的记录转到for_sale表中,并从err表中删除
		sql_del = "delete from for_sale_err where for_sale_property_id = " + str(data[0])
		self.cursor.execute(sql_del)
		self.db.commit()
		sql_insert ="INSERT for_sale (for_sale_property_id,price,area,floor_index,title,spatial_arrangement,total_floor,builded_year,advantage,total_price,\
				details_url,community_name,first_acquisition_time,from_,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		self.cursor.execute(sql_insert,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],comm_id))
		self.db.commit()


if __name__=="__main__":

	k = 0
	dupli = 1

	matchid = MatchIdFromErr()

	# comm_arr = matchid.get_comm_arr(u'Sheet3',matchid.exc)
	# load_arr = matchid.get_comm_arr(u'Sheet1',matchid.exc)
	comm_arr = matchid.get_comm_arr_fromMysql(0)
	load_arr = matchid.get_comm_arr_fromMysql(1)
	
	datas = matchid.get_datas()

	for data in datas:
		getid = matchid.get_id_from_arr(data,comm_arr)
		try:
			if len(getid) == 1:
				matchid.insert_for_sale(data,getid[0][2])
			elif len(getid) == 0:
				
				getroad = matchid.get_id_from_arr(data,load_arr)
				if len(getroad) == 1:
					matchid.insert_for_sale(data,getroad[0][2])
				elif len(getroad) == 0:
					# matchid.insert_err(data)
					pass
				elif len(getroad) > 1:
					matchid.handle_match_mul(data,getroad)
					
			elif len(getid) > 1:
				matchid.handle_match_mul(data,getid)
				
		
			k = k + 1

		except MySQLdb.Error,e:
			if e.args[0] == 1062 :
				print(str(dupli)+"aready have")
				dupli = dupli + 1

	matchid.close_db()