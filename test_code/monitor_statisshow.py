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
        self.time=self.get_time()
    # 非200数据
    def statis_err(self, task_id,time):
        self.dbcur()
        sql = "select create_time,api_id,resq_code,res_time,response from apirun_result where task_id=%s and resq_code not in(200,9001,9002,9003,9004) and create_time >%s order by resq_code" % (
            task_id,time)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

    # 超时数据
    def statis_timeout(self, task_id,time):
        self.dbcur()
        sql = "select create_time,api_id,resq_code,res_time,response from apirun_result where task_id=%s and res_time>10000 and create_time >%s order by resq_code" % (
        task_id, time)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

#
# if __name__ == '__main__':
#     a = StatisShow()
#     print(a.statis_timeout(48))
#     # main()
