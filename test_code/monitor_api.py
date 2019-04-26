#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from test_code.sqlop import *
# from sqlop import *

class Api_Monitor(SqlOperate):
    #接口相关函数

    global proll,idpro

    proll = {"APP":1,"产品库":2,"论坛":3,"资讯":4,"二手车":5,"经销商":6,"其他":7}
    idpro = {v : k for k, v in proll.items()}

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('monitor_db','host')
        self.user = conf.get('monitor_db','user')
        self.passwd = conf.get('monitor_db','passwd')
        self.database = conf.get('monitor_db','database')

    #插入数据
    def insdata(self,tablename,field_item):
        self.dbcur()
        sql = self.sqlInsert(tablename,field_item)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    #编辑数据
    def updata(self,tablename,field_itemm,condition):
        self.dbcur()
        sql = self.sqlUpdate(tablename,field_itemm,condition)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    #查询数据
    def seldata(self,tablename,fields,condition=10):
        self.dbcur()
        if condition != 10:
            sql = self.sqlSelect(tablename,fields,condition,repeat=1)
        else:
            sql = self.sqlSelect(tablename,fields,repeat=1)
        sql += ' order by id desc'
        self.sqlExe(sql)
        data = list(self.cur.fetchall())
        self.sqlclo()
        return data

    #app中新增接口的方法（post请求)
    def addapi(self,product,urlname,url,method,parm=0,check_point=0):
        proid = proll[product]
        self.insdata('api_list',{'urlname':urlname,'pro_id':proid,'url':url,'method':method,'check_point':check_point,'parameters_json':parm})

    #app中获取接口数据
    def getapi(self,apiid="all"):
        if apiid == "all":
            proname = self.seldata("api_list",['pro_id'])
            data = self.seldata("api_list",['id','urlname','url','method','parameters_json','status'],condition={'is_delete':0})
        else:
            proname = self.seldata("api_list",['pro_id'],condition={'id':apiid})
            data = self.seldata("api_list",['urlname','url','method','parameters_json','id'],condition={'id':apiid})
        prolist = []
        for i in proname:
            k = i[0]
            product = idpro[k]
            prolist.append(product)
        apidata = dict(zip(data,prolist))
        return apidata

    #app中修改接口内容(post请求)
    def editapi(self,url,urlname,product,method,apiid,parm=0):
        proid = proll[product]
        self.updata("api_list",{'urlname':urlname,'url':url,'parameters_json':parm,'pro_id':proid},condition={'id':apiid})

    #app中修改接口停用启用状态
    def apist(self,apiid):
        s = self.seldata("api_list",['status'],condition={'id':apiid})[0][0]
        if s == 0:
            s = 1
        else:
            s = 0
        self.updata("api_list",{'status':s},condition={'id':apiid})

    #app中修改接口显示状态
    def apishows(self,apiid):
        self.updata("api_list",{'is_delete':1},condition={'id':apiid})

    #获取项目下拉框内容
    def prolist(self):
        ll = list(idpro.values())
        return ll



# a = Api_Monitor()
# s = list(a.getapi(32).keys())
# print (s[0][3])



