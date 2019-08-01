# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-29 17:08:26

from test_code import *
from collections import Counter


class Monitor_Inform(SqlOperate):
    """接口监控策略"""

    def __init__(self):
        conf = configparser.ConfigParser()
        # conf.read("../static/conf/config.ini")
        conf.read("conf/config.ini")
        self.host = conf.get('monitor_db', 'host')
        self.user = conf.get('monitor_db', 'user')
        self.passwd = conf.get('monitor_db', 'passwd')
        self.database = conf.get('monitor_db', 'database')

    # 查询任务对应的策略次数、token、email
    def seltimes(self, taskid):
        self.dbcur()
        sql = "SELECT start_inform,stop_inform,re_inform,token,re_email FROM `task_list` WHERE id=%d " % (taskid)
        self.sqlExe(sql)
        data = list(self.cur.fetchall())
        self.sqlCom()
        self.sqlclo()
        return data[0]

    # 更新当前接口错误的次数
    def upnum(self, apiid, num):
        self.dbcur()
        sql = "UPDATE `api_inform` SET `inform`=%d where apiid = %d" % (num, apiid)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    # 是否发钉钉
    def start_inform(self, taskid, apiid, code):
        info = self.seltimes(taskid)
        if info[5] == 0:
            start_times = info[0]
            stop_times = info[1]
            re_times = info[2]
            token = info[3]
            receiver = info[4].split(",")

            self.dbcur()
            sql1 = "SELECT inform FROM `api_inform` WHERE apiid=%d " % (apiid)
            self.sqlExe(sql1)
            data = list(self.cur.fetchall())
            if data == []:
                sql1 = "INSERT INTO `api_inform` (`apiid`, `inform`) VALUES (%d, 0)" % (apiid)
                self.sqlExe(sql1)
                self.sqlCom()
                data = [(0,)]

            if str(code) != "200":
                num = data[0][0] + 1
            else:
                num = 0

            stopnum = start_times + stop_times
            renum = stopnum + re_times
            if num < start_times or renum > num >= stopnum:
                ding = 0
                content = ""
            elif start_times <= num < stopnum:
                ding = 1
                content = '''该接口已经报错,请相关人员及时修复 '''
            else:
                ding = 1
                content = '''该接口已经连续报错%d次''' % (num)
            return (ding, content, token, receiver, num)
        else:
            ding = 0
            return (ding,)

    def qq(self, taskid, apiid, code):
        info = self.start_inform(taskid, apiid, code)
        if info[0] == 1:
            content = "接口名称：%s \n 接口地址：%s \n 备注：%s + 详情信息……"
            self.sending(info[2], content)
            self.sendemail(info[3], info[1])
        self.upnum(apiid, info[4])


aa = Monitor_Inform()
aa.qq(8, 33, "200")
# aa.sendemail("aa")
