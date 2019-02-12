# -*- coding: utf-8 -*-
import pymysql
pymysql.install_as_MySQLdb


class  SqlOperate():
	"""数据库的基本操作"""

	def __init__(self):

		host = '192.168.0.20'
		user='test'
		passwd='jghAeuXL0x7npvSS'
		db='qa'

		self.db = pymysql.connect(host,user,passwd,db,charset='utf8')
		self.cur =self.db.cursor()


	#连接数据库，创建游标
	def dbcur(self):
		self.db = pymysql.connect('192.168.0.20','test','jghAeuXL0x7npvSS','qa',charset='utf8')
		self.cur =self.db.cursor()


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


	#执行sql
	def sqlExe(self,sqls):
		self.cur.execute(sqls)


	#提交sql
	def sqlCom(self):
		self.db.commit()


	# 关闭数据库连接
	def sqlclo(self):
		self.db.close()


	#插入数据:tablename:表名，field_item:插入的字段及内容
	def sqlInsert(self,tablename,field_item):
		insql = "insert into %s set "  %(tablename)
		insql += self.keyvalue(field_item)
		return insql


	#查询数据：tablename:表名，fields：查询的字段，返回数据列表
	def sqlSelect(self,tablename,fields):
		sesql = "select %s " % ','.join(fields)
		sesql += 'from %s ' %(tablename)
		return sesql


	#修改数据：tablename:表名，field_item:修改的字段及内容,condition:条件的字段内容（字典格式）
	def sqlUpdate(self,tablename,field_item,condition):
		upsql = "update %s set "  %(tablename) 
		upsql += '%s where %s' %(self.keyvalue(field_item),self.keyvalue(condition))
		return upsql




# a = SqlOperate()
# print (a.esoname','resostatus','name','notes']))
