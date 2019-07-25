import configparser
import time
import os
import platform
from test_code.sqlop import *

class Xmind_Upload(SqlOperate):
	#连接数据库
	def __init__(self):
		conf = configparser.ConfigParser()
		conf.read("conf/config.ini")
		self.host = conf.get('qa','host')
		self.user = conf.get('qa','user')
		self.passwd = conf.get('qa','passwd')
		self.database = conf.get('qa','database')

	#插入数据
	def fileinsert(self,filename):
		
		vesion =""
		beizhu =""
		str2 = "-"
		# str1[:str1.index(str2)]
		product = filename[:filename.index(str2)]
		# filename=filename.split('-')
		# for a in range(len(filename)):
		# 	product = filename[0]
		# 	work = filename[1]
		# 	vesion = filename[2]
		# 	if len(filename) < 4:
		# 	    beizhu = ""
		# 	else:
		# 		beizhu = filename[3]
		self.dbcur()
		sql = "INSERT INTO checklist (product,work,vesion,beizhu,addtime,updatetime)VALUES( '%s', '%s','%s','%s',curdate(),curdate())"%(product,filename,vesion,beizhu)
		self.sqlExe(sql)
		self.sqlCom()
		self.sqlclo()
		return "pass"	
	#文件上传
	def fileupload(self,f):
		way = ""
		if(platform.system()=='Windows'):
			way = "C:/Users/360che/Desktop/check_point/tmp/"
		elif(platform.system()=='Linux'):
			way = "/data/check_point/xmind/"
		basepath = os.path.dirname(__file__)  # 当前文件所在路径
		upload_path = os.path.join(basepath, way,f.filename)#secure_filename(f.filename)
		upload_path = os.path.abspath(upload_path) # 将路径转换为绝对路径
		f.save(upload_path)

	def filelist(self):
		way = ""
		if(platform.system()=='Windows'):
			way = "C:/Users/360che/Desktop/check_point/xls/"
		elif(platform.system()=='Linux'):
			way = "/data/check_point/xls/"
		filenames = os.listdir(way)
		a = []
		for filename in filenames:
			a.append(filename)
		return a