from test_code import *
import configparser
import requests
import time
import sys
import json
import pymysql


# 执行脚本类
class run(SqlOperate):
    '''
    参数为任务id
    run该任务下所有接口请求
    '''

    def __init__(self, task_id):
        self.task_id = task_id
        conf = configparser.ConfigParser()
        conf.read("/home/jinyue/test/conf/config.ini")
        # conf.read("../static/conf/config.ini")
        self.host = conf.get('monitor_db', 'host')
        self.user = conf.get('monitor_db', 'user')
        self.passwd = conf.get('monitor_db', 'passwd')
        self.database = conf.get('monitor_db', 'database')

    # 获取任务信息
    def get_taskinfo(self):
        self.dbcur()
        sql = "select * from task_list where id='%s'" % self.task_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = list(self.cur.fetchone())
        return data

    # 获取api信息
    def get_apiinfo(self, api_id):
        self.dbcur()
        sql = "select * from api_list where id=%s" % api_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data

    # 请求接口
    def run_api(self, url, method, params):
        try:
            if method == "GET":
                r = requests.get(url, params, timeout=(10, 10))
            elif method == "POST":
                r = requests.post(url, params, timeout=(10, 10))
            else:
                print("请求类型错误，目前只支持POST/GET")
            return r.status_code, r.elapsed.total_seconds() * 1000, r.text
        except requests.exceptions.ConnectTimeout as e:
            return 9001, 0, ("链接超时----%s" % e)
        except requests.exceptions.ReadTimeout as e:
            return 9002, 0, ("连接、读取超时----%s" % e)
        except requests.exceptions.ConnectionError as e:
            return 9003, 0, ("未知的服务器----%s" % e)

    # 结果入库
    def write_result(self, api_id, pro_id, task_id, resq_code, res_time, response):
        response = pymysql.escape_string(response)
        create_time = int(time.time())
        self.dbcur()
        sql = self.sqlInsert("apirun_result",
                             {"api_id": api_id, "pro_id": pro_id, "task_id": task_id, "resq_code": resq_code,
                              "res_time": res_time, "response": response, "create_time": create_time})
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    # 获取api执行结果信息
    def get_apire(self, api_id):
        self.dbcur()
        sql = "select * from apirun_result where api_id=%s order by create_time desc" % api_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data

    # 查询钉钉发送次数
    def dingcount(self, api_id, status=None):
        if status is None:
            self.dbcur()
            sql = "select status from api_list where id=%s" % api_id
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            data = self.cur.fetchone()
            return data
        else:
            self.dbcur()
            sql = "update api_list set status=status+1 where id=%s" % api_id
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            return 'ok'

    # 发钉钉
    def ding(self, api_id):
        data = self.get_apire(api_id)
        print(data)
        content = '''
任务id：%s
接口id：%s
响应码：%s
备注：详细信息请登录测试平台查看：http://127.0.0.1:5000/monitor/task_list
        ''' % (data[3], data[1], data[4])
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": [
                ],
                "isAtAll": "false"
            }
        }
        data = json.dumps(data)
        url = "https://oapi.dingtalk.com/robot/send?access_token=a0b3d4c7641ac2b7b4a16ce557331095fe1d9656ae9a5b6e7c86467ab0140410"
        HEADERS = {"Content-Type": "application/json ;charset=utf-8 "}
        count = int(self.dingcount(api_id)[0])
        if count <= 5 and count != 0:
            res = requests.post(url, data=data, headers=HEADERS)
            ret = "发钉钉结果：%s" % res.text
            self.dingcount(api_id, status=1)
        elif count == 0:
            ret = "未开启发送钉钉功能"
        else:
            ret = "发送超过5次"
        print(ret)

    # 主方法
    def main(self):
        api_list = self.get_taskinfo()[2][1:-1].split(",")
        for i in api_list:
            url = self.get_apiinfo(i)
            if not url:
                print("接口id：%s 不存在，跳过" % i)
                continue
            else:
                url = self.get_apiinfo(i)[3]
            method = self.get_apiinfo(i)[5]
            params = self.get_apiinfo(i)[7]
            api_id = self.get_apiinfo(i)[0]
            pro_id = self.get_apiinfo(i)[1]
            task_id = self.task_id
            resq_code, res_time, response = self.run_api(url, method, params)
            if resq_code != 200 and resq_code != 9001 and resq_code != 9002 and resq_code != 9003:
                self.write_result(api_id, pro_id, task_id, resq_code, res_time, response)
                self.ding(api_id)
            else:
                self.write_result(api_id, pro_id, task_id, resq_code, res_time, "ok")
        else:
            print("执行完成")


if __name__ == "__main__":
    task_id = sys.argv[1]
    run = run(task_id)
    run.main()
