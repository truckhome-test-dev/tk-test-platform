#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from test_code.sqlop import *


# from sqlop import *

class Api_Monitor(SqlOperate):
    # 接口相关函数

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('monitor_db', 'host')
        self.user = conf.get('monitor_db', 'user')
        self.passwd = conf.get('monitor_db', 'passwd')
        self.database = conf.get('monitor_db', 'database')

    # 插入数据
    def insdata(self, tablename, field_item):
        self.dbcur()
        sql = self.sqlInsert(tablename, field_item)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    # 编辑数据
    def updata(self, tablename, field_itemm, condition):
        self.dbcur()
        sql = self.sqlUpdate(tablename, field_itemm, condition)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    # 查询数据
    def seldata(self, tablename, fields, condition=10):
        self.dbcur()
        if condition != 10:
            sql = self.sqlSelect(tablename, fields, condition, repeat=1)
        else:
            sql = self.sqlSelect(tablename, fields, repeat=1)
        self.sqlExe(sql)
        data = list(self.cur.fetchall())
        self.sqlclo()
        return data

    # app中新增接口的方法（post请求)
    def addapi(self, product, urlname, url, method, parm=0, check_point=0):
        self.insdata('api_list',
                     {'urlname': urlname, 'pro_id': product, 'url': url, 'method': method, 'check_point': check_point,
                      'parameters_json': parm})

    # #app中获取接口数据
    def getapi(self, apiid="all", page=0):
        self.dbcur()
        print("apiid:",apiid)
        if apiid == "all":
            sql = "select a.id,a.urlname,a.url,p.name,a.method,a.parameters_json,a.status from api_list as a,product as p where a.pro_id = p.ID and a.is_delete = 0 order by id desc"
        else:
            sql = "select a.id,a.urlname,a.url,p.name,a.method,a.parameters_json from api_list as a,product as p where a.pro_id = p.ID and a.id = %s and a.is_delete = 0" % (
                apiid)
        sql += " limit %s,20" % str(int(page) * 20)
        print(sql)
        if page==-1:
            sql="select a.id,a.urlname,a.url,p.name,a.method,a.parameters_json,a.status from api_list as a,product as p where a.pro_id = p.ID and a.is_delete = 0 order by id desc"
        self.sqlExe(sql)
        data = list(self.cur.fetchall())
        self.sqlclo()
        return data

    # app中修改接口内容(post请求)
    def editapi(self, url, urlname, product, method, apiid, parm=0):
        proid = self.seldata("product", ['id'], condition={'name': product})[0][0]
        self.updata("api_list",
                    {'urlname': urlname, 'url': url, 'method': method, 'parameters_json': parm, 'pro_id': proid},
                    condition={'id': apiid})
        return id

    # app中修改接口停用启用状态
    def apist(self, apiid):
        s = self.seldata("api_list", ['status'], condition={'id': apiid})[0][0]
        if s == 0:
            s = 1
        else:
            s = 0
        self.updata("api_list", {'status': s}, condition={'id': apiid})

    # app中修改接口显示状态
    def apishows(self, apiid):
        self.updata("api_list", {'is_delete': 1}, condition={'id': apiid})

    # 获取项目下拉框内容
    def prolist(self):
        data = self.seldata("product", ['name', 'ID'])
        return data

    # 查询单个项目接口
    def proapi(self, proid,page=0):
        self.dbcur()
        if page==-1:
            sql = "select a.id,a.urlname,a.url,p.name,a.method,a.parameters_json,a.pro_id from api_list as a,product as p where a.pro_id = p.ID and a.pro_id = %s and a.is_delete = 0" % (
                proid)
        else:
            sql = "select a.id,a.urlname,a.url,p.name,a.method,a.parameters_json,a.pro_id from api_list as a,product as p where a.pro_id = p.ID and a.pro_id = %s and a.is_delete = 0" % (
                proid)
            sql += " limit %s,30" % str(int(page) * 30)#数据库进行分页查询，使用limit方法每页30条数据
        self.sqlExe(sql)
        data = list(self.cur.fetchall())
        self.sqlclo()
        return data

    def proname(self, id):
        data = self.seldata("product", ['name'], condition={'ID': id})
        return data[0][0]

# a = Api_Monitor()
# print (a.getapi(page=1))
