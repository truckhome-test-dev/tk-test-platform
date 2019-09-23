#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2019/9/17 19:30
# @Author  : Mr. Cui
# @File    : monitor_statisshow.py
# @Software: PyCharm
from test_code import *


class StatisShow(StatisPush):
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('monitor_db', 'host')
        self.user = conf.get('monitor_db', 'user')
        self.passwd = conf.get('monitor_db', 'passwd')
        self.database = conf.get('monitor_db', 'database')
        self.time = self.get_time()

    def str_to_time(self, timeStamp):
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    # 非200数据
    def statis_err(self, task_id, time):
        self.dbcur()
        sql = "select create_time,api_id,resq_code,res_time,response,FROM_UNIXTIME(create_time,'%%Y-%%m-%%d %%H:%%i:%%s') from apirun_result where task_id=%s and resq_code not in(200,9001,9002,9003,9004) and (create_time between %s and %s) order by resq_code" % (
            task_id, time, str(int(time) + 96400))
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        mm = Monitor_Mongodb()
        l = []
        for i in data:
            l1 = list(i)
            title = mm.get_interface_name(i[1])
            project_id = mm.get_project_id(i[1])
            l1.append(title)
            l1.append(project_id)
            l.append(l1)
        return l

    # 超时数据
    def statis_timeout(self, task_id, time):
        self.dbcur()
        sql = "select create_time,api_id,resq_code,res_time,response,FROM_UNIXTIME(create_time,'%%Y-%%m-%%d %%H:%%i:%%s') from apirun_result where task_id=%s and res_time>10000 and (create_time between %s and %s) order by resq_code" % (
            task_id, time, str(int(time) + 96400))
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        mm = Monitor_Mongodb()
        l = []
        for i in data:
            l1 = list(i)
            title = mm.get_interface_name(i[1])
            project_id = mm.get_project_id(i[1])
            l1.append(title)
            l1.append(project_id)
            l.append(l1)
        return l

#
# if __name__ == '__main__':
#     a = StatisShow()
#     print(a.statis_timeout(48))
#     # main()
