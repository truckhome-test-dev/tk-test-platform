#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from test_code.sqlop import * 
# from sqlop import * 

class Device_Manag(SqlOperate):
	#资源管理Resou_Manag


	#插入数据
	def insData(self,tablename,field_item):
		self.dbcur()
		sql = self.sqlInsert(tablename,field_item)
		self.sqlExe(sql)
		self.sqlCom()
		self.sqlclo()


	#编辑数据
	def upData(self,tablename,field_itemm,condition):
		self.dbcur()
		sql = self.sqlUpdate(tablename,field_itemm,condition)
		self.sqlExe(sql)
		self.sqlCom()		
		self.sqlclo()


	#查询数据
	def selData(self,tablename,fields,condition=10,repeat=0,indexs=11):
		self.dbcur()
		if condition != 10:
			sql = self.sqlSelect(tablename,fields,condition)
		else:
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


	def appinsp(self,devname,devtype,name=0,devnotes=0):
		if devtype == "手机":
			devtype = 0
		else :
			devtype = 1
		self.insData('devices',{'devname':devname,'devtype':devtype,'name':name,'notes':devnotes})
		return "pass"


	def appseap(self,param):
		seadev = json.loads(param)['searchdev']
		alldata = str(self.selData('devices',['devname','devstatus','name','notes','ID'],condition={'devname':seadev}))
		return alldata


	def appdelp(self,param):
		devdata = json.loads(param)
		self.upData('devices',{'status':devdata['status']},{'ID':devdata['devid']})
		return 'ok'

	def appga(self):
		data = self.selData('devices',['devname','devstatus','name','notes','ID'],condition={'status':0})
		return data


	def appgd(self):
		data = self.selData('devices',['devname'],condition={'status':0},indexs=1)
		return data
	
	
	def appeditg(self,devid):
		data = self.selData('devices',['devname','devstatus','name','notes','ID'],condition={'ID':devid})
		data = list(data[0])
		return data


	def appeditp(self,devname,devst,name,notes,condition):
		self.upData('devices',{'devname':devname,'devstatus':devst,'name':name,'notes':notes},{'ID':condition})
		return 'ok'


# q = Device_Manag()
# print (q.appseap({'searchdev':"iPhone6s"}))
# print(type(q.appeditp(37)))
# print (type(q.selData('devices',['devname','devstatus','name','notes'],condition={'devname':"荣耀"})))
# q.upData('devices',{'status':1},{'ID':32})

