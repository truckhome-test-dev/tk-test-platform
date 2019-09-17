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

    def cha_only(self,id):
        self.dbcur()
        sql = "SELECT * FROM `project_pp` WHERE id = %s"%id
        self.sqlExe(sql)
        data = self.cur.fetchone()
        self.sqlclo()
        # print(data)
        return data


    def edit(self,id,Business,Product,PM,Business_type,DMP,QD_Dev,HD_Dev,DEV_Leader,qa,Platform):
        self.dbcur()
        sql = "UPDATE `project_pp` SET `Business` = '%s',`Product` = '%s',`PM` = '%s',`Business_type` = '%s',`DMP` = '%s',`QD_Dev` = '%s',`HD_Dev` = '%s',`DEV_Leader` = '%s',`qa` = '%s',`Platform` = '%s' WHERE `project_pp`.`id` = '%s'"%(Business,Product,PM,Business_type,DMP,QD_Dev,HD_Dev,DEV_Leader,qa,Platform,id)
        print (sql)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        # print(data)
        # return data

    def added(self,Business,Product,PM,Business_type,DMP,QD_Dev,HD_Dev,DEV_Leader,qa,Platform):
        self.dbcur()
        sql = "INSERT INTO `project_pp` (`Business`, `Product`, `PM`, `Business_type`,`DMP`, `QD_Dev`, `HD_Dev`, `DEV_Leader`, `QA`, `Platform`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(Business,Product,PM,Business_type,DMP,QD_Dev,HD_Dev,DEV_Leader,qa,Platform)
        print (sql)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()


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
            # print(sql)
            self.sqlExe(sql)
            data = list(self.cur.fetchall())
            self.sqlclo()
            # print(data)
            return data

# a = Cha_Project()
# a.edit(45,'资讯啊啊','资讯平台','马美琪','C端','鲁莹莹、田一婷','余尚辉、赵伟、杜帧帧、于风磊、王京','王伟龙、张磊磊、欧阳昊、张明、刘哲','杨毓平','何丹','PC、App、M、微信')