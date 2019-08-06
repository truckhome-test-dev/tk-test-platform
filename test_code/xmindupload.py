import configparser
import time
import os
import platform
from test_code.sqlop import *
from xmindparser import xmind_to_dict, xmind_to_xml, xmind_to_json
from test_code.to_xls import *
import re

class Xmind_Upload(SqlOperate):
	#连接数据库
	def __init__(self):
		conf = configparser.ConfigParser()
		conf.read("conf/config.ini")
		self.host = conf.get('qa','host')
		self.user = conf.get('qa','user')
		self.passwd = conf.get('qa','passwd')
		self.database = conf.get('qa','database')

	#插入TestCase表（业务线、文件名）
	def fileinsert(self,filename,content):
		#业务线
		product = filename[:filename.index("-")]
		#文件名
		filenames = filename[0:-6]
		filenames+=".xls"
		#dict内容
		result = self.sel(filenames)
		self.dbcur()
		sql = ""
		if result:
			sql = 'update checklist SET product="%s",filenames="%s",content="%s",addtime=curdate() WHERE filenames="%s"'%(product,filenames,content,filenames)
		else:
			sql = 'INSERT INTO checklist (product,filenames,content,addtime)VALUES( "%s","%s","%s",curdate())'%(product,filenames,content)
		self.sqlExe(sql)
		self.sqlCom()
		self.sqlclo()
		return "pass"

	#判断该数据是否存在
	def sel(self,filename):
		self.dbcur()
		sql = "select filenames from checklist where filenames ='%s'"% filename
		self.sqlExe(sql)
		self.sqlCom()
		self.sqlclo()
		data = self.cur.fetchall()
		return data

	#筛选查询
	def sel_file(self,product):
		self.dbcur()
		sql = "select filenames from checklist where product ='%s'"% product
		self.sqlExe(sql)
		self.sqlCom()
		self.sqlclo()
		data = self.cur.fetchall()
		return data

    #全量查询所有文件名
	def fileselect(self):
		self.dbcur()
		sql = "select filenames from checklist"
		self.sqlExe(sql)
		self.sqlCom()
		self.sqlclo()
		data = self.cur.fetchall()
		l = []
		for i in data:
			l.append(i[0])
		return l


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
    #读取xls文件下的所有文件
	def filelist(self):
		way = ""
		if(platform.system()=='Windows'):
			way = "C:/Users/360che/Desktop/check_point/tmp/"
		elif(platform.system()=='Linux'):
			way = "/data/check_point/xls/"
		filenames = os.listdir(way)
		a = []
		for filename in filenames:
			a.append(filename)
		return a

	def to_dict(self,path):
		data = xmind_to_dict(path)
		a_str = str(data)
		data_dict = eval(a_str.replace('"','“'))
		return data_dict

    #查询文件内容
	def filedata(self,filename):
		self.dbcur()
		sql = "select content from checklist where filenames = '%s'"%filename
		self.sqlExe(sql)
		self.sqlCom()
		self.sqlclo()
		data = self.cur.fetchall()
		l = ""
		for i in data:
			l=i[0]
		dict_data =self.to_line(l)
		dict_data = eval(dict_data)
		
		return dict_data
		
	#下载excel
	def downexcel(self,filename):
		data_dict = self.filedata(filename)
		x_c = filename[0:-4]
		x_a = xmind_to_xx(data_dict,filename, x_c)
		x_a.to_excel(x_a.data_dict[0]['topic'])
		x_a.save_xls()
		#合并单元格
		x_b = style_excel(self.xls_way(), x_c+'.xls', x_a.data_dict[0]['topic']['title'])
		x_b.merge_excel(x_b.calculate())
		x_b.save_style_excel(self.xls_way()+x_c+'.xls')
		return "pass"

	#文件上传路径
	def xmind_way(self):
		way = ""
		if(platform.system()=='Windows'):
			way ="C:/Users/360che/Desktop/check_point/tmp/"
		elif(platform.system()=='Linux'):
			way ="/data/check_point/xmind/" 
		return way          

	#文件下载路劲
	def xls_way(self):
		way_xls = ""
		if(platform.system()=='Windows'):
			way_xls = "C:/Users/360che/Desktop/check_point/xls/"
		elif(platform.system()=='Linux'):
			way_xls = "/data/check_point/xls/"
		return way_xls

	#判断xls文件是否存在
	def xls_true(self,filename):
		path = self.xls_way()+filename
		os.path.exists(path)

	def to_line(self,s):
		d = {'\r':'###','\n':'***'} 
		if '\r' in s:
			for i,o in d.items():
				n = s.replace(i,o)
				s = n
		else:
			for o,i in d.items():
				n = s.replace(i,o)
				s = n
		return s