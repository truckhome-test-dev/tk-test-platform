#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2019/9/16 19:48
# @Author  : Mr. Cui
# @File    : monitor_statispush.py
# @Software: PyCharm
import os, sys

sys.path.append('../')
from test_code import *
import configparser
import time
import json
import requests


class StatisPush(SqlOperate):

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("../conf/config.ini")
        self.host = conf.get('monitor_db', 'host')
        self.user = conf.get('monitor_db', 'user')
        self.passwd = conf.get('monitor_db', 'passwd')
        self.database = conf.get('monitor_db', 'database')
        self.time = self.get_time()

    # 获取前一天下午6点时间戳
    def get_time(self):
        """
        :return: 1568541600
        """
        # 获取当天23：59:59时间戳
        t = time.localtime(time.time())
        time1 = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S')))
        time1 = time1 - 60 * 60 * 6
        return time1

    # 获取任务信息
    def get_taskinfo(self):
        self.dbcur()
        sql = "select id,token,task_name from task_list where is_delete=0 and status=1"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

    # 非200次数
    def statis_err_count(self, task_id):
        self.dbcur()
        sql = "select resq_code,count(resq_code) from apirun_result where task_id=%s and resq_code not in(200,9001,9002,9003,9004) and (create_time between %s and %s) group by resq_code" % (
            task_id, self.time, self.time + 86400)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        if len(data) == 0:
            ret = ""
        else:
            ret = ""
            for i in data:
                ret += str(i[0]) + "次数:" + str(i[1]) + "\n"
        return ret

    # 超时次数
    def statis_timeout_count(self, task_id):
        self.dbcur()
        sql = "select count(*) from apirun_result where task_id=%s and res_time>10000 and (create_time between %s and %s)" % (
            task_id, self.time, self.time + 86400)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data[0]

    def sending(self, token, content):
        HEADERS = {"Content-Type": "application/json ;charset=utf-8 "}
        data = {"msgtype": "text", "text": {"content": content}, "at": {"atMobiles": [], "isAtAll": "false"}}
        data = json.dumps(data)
        res = requests.post(token, data=data, headers=HEADERS)


def main():
    a = StatisPush()
    for i, j ,k in a.get_taskinfo():
        err_count = a.statis_err_count(i)
        time_out_count = a.statis_timeout_count(i)
        content = "今日接口统计：\n任务名称：%s\n%s超时次数(10s)：%d\n查看详情：http://qa.kcimg.cn/monitor/statis_show?task_id=%s&time=%s" % (
            k,err_count, time_out_count, i, a.time)
        print(j, content)
        a.sending(j,content) #调试时注释掉此行，不然会发送正式钉钉群消息


if __name__ == '__main__':
    # a=StatisPush()
    # print(a.time)
    # print(a.statis_err(46))
    main()
