#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-29 17:08:26
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
import random


class Scheduling(object):
    """docstring for Test_Tools_Api"""

    def __init__(self):
        today = datetime.date.today()
        next_months = today - relativedelta(months=-1)
        cookies = {'X360CHE_password': '4665afe6cd25c35251a331c576f3b154', 'X360CHE_uid': '42'}
        url = 'https://connection.360che.com/server/admin.php/Task/ganTe'
        data = {'start_date': today, 'end_date': next_months, 'department_id': '18'}
        # test
        # url = 'http://venus.360che.com/server/admin.php/Task/ganTe'
        # data = {'start_date':today, 'end_date':next_months, 'department_id':'0'}
        self.paiqi_json = requests.post(url, data=data, cookies=cookies)

    # print(self.paiqi_json.json())

    def get_data(self):
        # 获取所有排期
        today = datetime.datetime.today()
        next_months = today - relativedelta(months=-1)
        return self.paiqi_json.json()

    def get_date(self):
        # 整理日期格式为['1月1日'，’1月2日]
        date = self.get_data()['data']['dateArr']
        self.week = self.get_data()['data']['weekArr']
        dateList = []
        for i, o in date['2019'].items():
            for x in o:
                datestr = ''
                datestr = i + '-' + str(x)
                dateList.append(datestr)
        for i in self.week[:12]:
            dateList[i['x']] = 'weekend'
        return dateList[:12]

    def get_task(self):
        # 获取任务,并整理数据格式为{QA：[task1,task2,[colour]]}
        taskArr = self.get_data()['data']['userTask']
        taskList = {}
        colour = ['#F0F8FF', '#FAEBD7', '#7FFFD4', '#8A2BE2', '#5F9EA0', '#87CEEB', '#FF8C00', '#FFD700', '#CD5C5C',
                  '#FFFACD', '#87CEFA', '#FFA500', '#FFB6C1', '#FFEBCD', '#FF9900', '#9ACD32']
        for auser in taskArr:
            for atask in auser['listArr']:
                QAname = auser['name'].split('[')[0]
                if QAname not in taskList:
                    taskList[QAname] = []
                task = self._dis_task(atask['name'], atask['day'])
                if task.count('') == 12:
                    continue
                for i in self.week[:11]:
                    if i['x'] <= 11:
                        task[i['x']] = ''
                task.append(random.sample(colour, 1))
                taskList[QAname].append(task)
        return taskList

    def date_rest(self):
        # 获取任务个数
        task = {}
        date = self.get_date()
        for i, o in self.get_task().items():
            task[i] = {len(o): o}
        data = {'day': date, 'task': task}
        return data

    def _dis_task(self, name, day):
        # 计算排期
        if len(day) == 1:
            return self._r_task(day[0]['x'], day[0]['y'], name)
        else:
            return self._r_tasks(day, name)

    def _r_task(self, index, num, taskname):
        # 整理单个排期的数据格式
        l = []
        for i in range(0, index):
            l.append('')
        for i in range(index, index + num):
            l.append(taskname)
        for i in range(index + num, 31):
            l.append('')
        return l[:12]

    def _r_tasks(self, day, taskname):
        # 整理多个排期的数据格式
        nothing = self._r_tasks_l(day)
        l = []
        for i in range(0, day[0]['x']):
            l.append('')
        for i in range(day[0]['x'], day[0]['x'] + (day[-1]['x'] + day[-1]['y'])):
            l.append(taskname)
        for i in range((day[-1]['x'] + day[-1]['y']), 31):
            l.append('')
        for i in nothing:
            l[i] = ''
        return l[:12]

    def _r_tasks_l(self, day):
        # 整理之间空白的排期
        nothing = []
        for d in range(0, len(day) - 1):
            nothing = nothing + [x for x in range((day[d]['x'] + day[d]['y']), day[d + 1]['x'])]
        return nothing
