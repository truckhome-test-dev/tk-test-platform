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
        :param api_id:
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

    #编辑任务
    def task_edit(self,id,task_name,api_id,frequency,status,is_delete):
        pass



    #删除定时任务
    def timingtask_del(task_id):
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
    def timingtask_add(task_id,frequency):
        '''
        :param task_id:
        :param frequency:
        :return:
        */10 * * * * /usr/sbin/ntpdate ntp3.aliyun.com
        #* * * * * /root/.pyenv/shims/python /home/jinyue/tk-test-platform/test_code/monitor_run.py 1 >> /home/jinyue/tk-test-platform/test_code/load.log
        '''
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

if __name__=="__main__":
    a=Monitor_Task()
    a.task_add(6,[1,2,3],1)