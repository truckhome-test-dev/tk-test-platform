# -*- coding: utf-8 -*-
from test_code.sqlop import *
# from sqlop import *

import configparser


class Cha_Project(SqlOperate):
    def __init__(self):
        conf = configparser.ConfigParser()
        # conf.read("../static/conf/config.ini")
        conf.read("conf/config.ini")
        self.host = conf.get('qa', 'host')
        self.user = conf.get('qa', 'user')
        self.passwd = conf.get('qa', 'passwd')
        self.database = conf.get('qa', 'database')

    def cha(self, all=None):
        if all == None or all == '':
            self.dbcur()
            sql = "SELECT * FROM project_pp"
            self.sqlExe(sql)
            data = list(self.cur.fetchall())
            self.sqlclo()
            return data
        else:
            self.dbcur()
            sql = "SELECT * FROM `project_pp` WHERE concat(id,Business,Product,PM,DMP,QD_Dev,HD_Dev,DEV_Leader,qa,Platform)like '%" + all + "%'"
            print(sql)
            self.sqlExe(sql)
            data = list(self.cur.fetchall())
            self.sqlclo()
            return data
# a = Cha_Project()
# a.cha('王京')
