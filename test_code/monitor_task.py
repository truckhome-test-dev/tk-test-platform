from test_code.sqlop import *
# from sqlop import *
import configparser
import requests
import time
import sys
import os

class Monitor_Task(SqlOperate):
    '''
    任务相关方法
    '''
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("../static/conf/config.ini")
        self.host = conf.get('monitor_db','host')
        self.user = conf.get('monitor_db','user')
        self.passwd = conf.get('monitor_db','passwd')
        self.database = conf.get('monitor_db','database')

    #添加任务
    def task_add(self,task_name,api_id,frequency):
        '''
        :param task_name:
        :param api_id:列表
        :param frequency:
        :return:
        '''
        create_time = int(time.time())
        self.dbcur()
        sql=self.sqlInsert("task_list",
                           {"task_name":task_name,"api_id":api_id,"frequency":frequency,"create_time":create_time,"update_time":create_time})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret= "add task success"
        except pymysql.err.IntegrityError as e:
            ret= e
        return ret

    #任务列表
    def task_list(self):
        '''
        不需要参数
        :return: (('APP', None, '', 0), ('产品库', None, '', 0), ('互动', None, '60s', 0)）
        '''
        self.dbcur()
        sql=self.sqlSelect("task_list",["task_name","api_id","frequency","status"],condition={"is_delete":0},repeat="1")
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data=self.cur.fetchall()
        return data

    #任务详情
    def task_info(self,task_id):
        '''
        :param task_id:
        :return: ('论坛', '[1,32,34]', '20',1)/不存在返回None
        '''
        self.dbcur()
        sql = "select task_name,api_id,frequency,status from task_list where id='%s'" % task_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data

    #编辑任务
    def task_edit(self,task_id,task_name,api_id,frequency):
        '''
        :param id:
        :param task_name:
        :param api_id:
        :param frequency:
        :return:
        '''
        data=self.task_info(task_id)
        if data is None:
            return "任务id不存在"
        self.dbcur()
        sql = self.sqlUpdate("task_list",{"task_name":task_name,"api_id":api_id,"frequency":frequency},{"id":task_id})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret= "edit task success"
        except pymysql.err.IntegrityError as e:
            ret= e
        return ret

    #修改任务状态
    def task_status(self,task_id,status):
        '''
        :param task_id:
        :return:
        '''
        data=self.task_info(task_id)
        if data is None:
            return "任务id不存在"
        self.dbcur()
        sql = self.sqlUpdate("task_list",{"status":status},{"id":task_id})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret= "edit task status success"
        except pymysql.err.IntegrityError as e:
            ret= e
        return ret

    #删除任务
    def task_del(self,task_id):
        '''
        :param task_id:
        :return:
        '''

        data=self.task_info(task_id)
        if data is None:
            return "任务id不存在"
        self.dbcur()
        sql = self.sqlUpdate("task_list",{"is_delete":1},{"id":task_id})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret= "del task success"
        except pymysql.err.IntegrityError as e:
            ret= e
        return ret

    #删除定时任务
    def timingtask_del(self,task_id):
        '''
        :param task_id:
        :return:
        '''
        data="monitor_run.py %d"%task_id
        with open("/var/spool/cron/root", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("/var/spool/cron/root", "w", encoding="utf-8") as f_w:
            for line in lines:
                if data in line:
                    continue
                f_w.write(line)

    #添加定时任务
    def timingtask_add(self,task_id):
        '''
        :param task_id:
        :param frequency:
        :return:"task_id已存在"/"添加定时任务成功"
        */10 * * * * /usr/sbin/ntpdate ntp3.aliyun.com
        #* * * * * /root/.pyenv/shims/python /home/jinyue/tk-test-platform/test_code/monitor_run.py 1 >> /home/jinyue/tk-test-platform/test_code/load.log
        '''
        frequency=self.task_info(task_id)[2]
        data="*/%d * * * * /root/.pyenv/shims/python /home/jinyue/tk-test-platform/test_code/monitor_run.py %d >> /home/jinyue/tk-test-platform/test_code/task.log"%(frequency,task_id)
        data_task="monitor_run.py %d"%task_id
        with open("/var/spool/cron/root", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("/var/spool/cron/root", "a", encoding="utf-8") as f_w:
            for line in lines:
                if data_task in line:
                    ret="task_id已存在"
                    break
            else:
                f_w.write(data)
                ret="添加定时任务成功"
            return ret

    #启动停止任务
    def run(self,task_id):
        '''
        :param task_id:
        :return:1->0/ 0->1
        '''
        status=self.task_info(task_id)[3]
        if status is None:
            return "任务id不存在"
        elif status==1:
            self.task_status(task_id, 0)
            self.timingtask_add(task_id)
        elif status==0:
            self.task_status(task_id, 1)
            self.timingtask_del(task_id)
        return "ok"


if __name__=="__main__":
    a=Monitor_Task()
    print(a.run(1))