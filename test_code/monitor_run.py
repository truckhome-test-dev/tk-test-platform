from test_code.sqlop import *
import configparser
import requests

#执行脚本类
class run(SqlOperate):
    '''
    参数为任务id
    run该任务下所有接口请求
    '''
    def __init__(self,task_id):
        self.task_id=task_id
        conf = configparser.ConfigParser()
        conf.read("../static/conf/config.ini")
        self.host = conf.get('monitor_db','host')
        self.user = conf.get('monitor_db','user')
        self.passwd = conf.get('monitor_db','passwd')
        self.database = conf.get('monitor_db','database')

#获取任务信息
    def get_taskinfo(self):
        self.dbcur()
        sql = "select * from task_list where id=%s" % self.task_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data

#获取api信息
    def get_apiinfo(self,api_id):
        self.dbcur()
        sql = "select * from api_list where id=%s" % api_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data


#请求接口
    def run_api(self,url,method,params):
        if method=="GET":
            r = requests.get(url, params)
        elif method=="POST":
            r = requests.post(url, params)
        else:
            print("请求类型错误，目前只支持POST/GET")
        return r.text



a=run(1)
print(a.get_apiinfo(1))
