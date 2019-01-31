#!/usr/bin/env python
# -*- coding: utf-8 -*-


from test_code.sqlop import * 
# from sqlop import * 

class Device_Manag(SqlOperate):
	#资源管理Resou_Manag


	#插入数据
	def insData(self,tablename,field_item):
		sql = self.sqlInsert(tablename,field_item)
		self.sqlExe(sql)
		self.sqlCom()


	#删除数据
	def delData(self,tablename,field_itemm,condition):
		sql = self.sqlUpdate(tablename,field_itemm,condition)
		self.sqlExe(sql)
		self.sqlCom()		


	#查询数据
	def selData(self,tablename,fields,indexs=11):
		self.dbcur()
		sql = self.sqlSelect(tablename,fields)
		sql += ' order by ID desc'
		self.sqlExe(sql)
		data = list(self.cur.fetchall())
		ll = []
		if indexs == 11:
			ll = data
		else:
			for i in data:
				for j in range(indexs):
					ll.append(list(i)[j])

		self.sqlclo()
		return ll


# q = Device_Manag()
# print (q.selData('devices',['devname','devstatus'],2))
