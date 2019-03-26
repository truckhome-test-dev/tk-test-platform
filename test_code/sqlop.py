# -*- coding: utf-8 -*-
import pymysql
pymysql.install_as_MySQLdb


class  SqlOperate():
	"""数据库的基本操作"""

	def __init__(self, host='192.168.0.20', user='test', passwd='jghAeuXL0x7npvSS', database='qa'):
			self.host = host
			self.user = user
			self.passwd = passwd
			self.database = database


	#连接数据库，创建游标
	def dbcur(self):
		self.db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
		self.cur = self.db.cursor()


	def keyvalue(self,field_item):
		"""
		将字典变成，key='value',key='value' 的形式,
		field_item：{字段名:字段值},字典格式
		"""
		fieldlist = []
		for k, v in field_item.items():
			tmp = "%s='%s'" % (str(k), str(v))
			fieldlist.append(tmp)
		return (','.join(fieldlist))


	def keyvalue2(self,field_item):
		"""
		将字典变成，key='value' and key='value' 的形式,
		field_item：{字段名:字段值},字典格式
		"""
		fieldlist = []
		for k, v in field_item.items():
			tmp = "%s='%s'" % (str(k), str(v))
			fieldlist.append(tmp)
		return (' and '.join(fieldlist))


	#执行sql
	def sqlExe(self,sqls):
		self.cur.execute(sqls)


	#提交sql
	def sqlCom(self):
		self.db.commit()


	# 关闭数据库连接
	def sqlclo(self):
		self.db.close()


	def sqlInsert(self,tablename,field_item):
		"""插入数据
			tablename:表名，
			field_item:插入的字段及内容，字典格式{'字段名称':'字段内容'}
		"""
		insql = "insert into %s set "  %(tablename)
		insql += self.keyvalue(field_item)
		return insql


	def sqlSelect(self,tablename,fields,condition=10,repeat=0):
		"""	查询数据
		tablename:表名，
		fields：查询的字段，[字段名称]
		condition:查询条件，默认无条件，条件格式：{'字段名称':字段内容}
		repeat:是否去重，默认去重
		"""
		sesql = "select %s " % ','.join(fields)
		sesql += ' from %s ' %(tablename)	
		if condition != 10:
			sesql += ' where %s' %(self.keyvalue(condition))
		if repeat == 0:
			sesql += ' group by devname'		
		return sesql
 

	def sqlUpdate(self,tablename,field_item,condition):
		"""修改数据
		tablename:表名，
		field_item:修改的字段及内容,格式：{'字段名称':修改内容}
		condition:条件格式：{'字段名称':字段内容}
		"""	
		upsql = "update %s set "  %(tablename) 
		upsql += '%s where %s' %(self.keyvalue(field_item),self.keyvalue2(condition))
		return upsql


