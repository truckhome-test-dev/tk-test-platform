from test_code.sqlop import *
import configparser
import requests
import time

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
        try:
            if method=="GET":
                r = requests.get(url, params,timeout=(10,10))
            elif method=="POST":
                r = requests.post(url, params,timeout=(10,10))
            else:
                print("请求类型错误，目前只支持POST/GET")
            return r.status_code,r.elapsed.total_seconds()
        except requests.exceptions.ReadTimeout as e:
            return 504,"超时"

    def api_result(self,api_id,pro_id,task_id,resq_code,res_time,err_info=None):
        create_time = int(time.time())
        self.dbcur()
        sql=self.sqlInsert("apirun_result",
                           {"api_id":api_id,"pro_id":pro_id,"task_id":task_id,"resq_code":resq_code,"res_time":res_time,"err_info":err_info,"create_time":create_time})



    def main(self):
        api_list=self.get_taskinfo()[2].split(",")
        for i in api_list:
            url=self.get_apiinfo(i)[3]
            method=self.get_apiinfo(i)[5]
            params=self.get_apiinfo(i)[7]
            a=self.run_api(url,method,params)
            print(a)
        else:
            print("执行完成")

# if __name__=="__main__":
#     run.main()


a=run(1)
print(a.api_result())
