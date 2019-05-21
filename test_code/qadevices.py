#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import configparser
from test_code.sqlop import *


# from sqlop import*


class Device_Manag(SqlOperate):
    # 资源管理Resou_Manag

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('qa', 'host')
        self.user = conf.get('qa', 'user')
        self.passwd = conf.get('qa', 'passwd')
        self.database = conf.get('qa', 'database')

    # 插入数据
    def insData(self, tablename, field_item):
        self.dbcur()
        sql = self.sqlInsert(tablename, field_item)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    # 编辑数据
    def upData(self, tablename, field_itemm, condition):
        self.dbcur()
        sql = self.sqlUpdate(tablename, field_itemm, condition)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    # 查询数据
    def selData(self, tablename, fields, condition=10, repeat=0, indexs=11):
        self.dbcur()
        if condition != 10:
            sql = self.sqlSelect(tablename, fields, condition)
        else:
            sql = self.sqlSelect(tablename, fields)
        sql += ' order by ID asc'
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

    # 插入数据路由
    def appinsp(self, devname, name=0, devnotes=0, deversion=0, devtype=0, devsystem=0):
        self.insData('devices',
                     {'devname': devname, 'devtype': devtype, 'name': name, 'notes': devnotes, 'version': deversion,
                      'devsystem': devsystem})
        return "pass"

    # 查询数据路由所有
    def appga(self, devtype=2):
        if devtype != 0 and devtype != 1:
            data = self.selData('devices',
                                ['ID', 'devname', 'status', 'username', 'version', 'notes', 'devtype', 'devsystem'])
        else:
            data = self.selData('devices',
                                ['ID', 'devname', 'status', 'username', 'version', 'notes', 'devtype', 'devsystem'],
                                condition={'devtype': devtype})
        data.sort(key=lambda x: x[7])
        return data

    # 更新使用状态
    def appusep(self, devid, name):
        data = self.selData('devices', ['devname', 'status'], condition={'ID': devid})
        devname = data[0][0]
        if data[0][1] == 1:
            name2 = "无"
            devst = 0
            self.upData('devices', {'status': devst, 'username': name2}, {'ID': devid})
        else:
            devst = 1
            self.upData('devices', {'status': devst, 'username': name}, {'ID': devid})
        self.inslog(devid, devname, name, devst)

    # 记录日志
    def inslog(self, devid, devname, name, devst):
        timeq = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if devst == 1:
            self.insData('devuse',
                         {'devid': devid, 'devname': devname, 'status': devst, 'user': name, 'usetime': timeq})
        else:
            self.upData('devuse', {'retime': timeq, 'backer': name, 'status': 0}, {'devid': devid, 'status': 1})

# a = Device_Manag()
# list = a.appga()
# print (list)
