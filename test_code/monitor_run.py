import sys

sys.path.append('../')
from test_code import *


# 获取mongo数据
class get_md():
    def __init__(self):
        self.conn = pymongo.MongoClient('192.168.2.1', 27017)
        self.db = self.conn.yapi

    # 获取domain
    def get_domain(self, interface_id):
        myset = self.db.interface
        data = myset.find({"_id": int(interface_id)}, {"project_id": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            project_id = L[0]["project_id"]
        else:
            project_id = None
        myset = self.db.project
        data = myset.find({"env": {"$elemMatch": {"name": "正式环境"}}, "_id": int(project_id)},
                          {"env": {"$elemMatch": {"name": "正式环境"}}})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            data = L[0]["env"][0]["domain"]
        else:
            data = None
        return data

    # 获取method
    def get_method(self, interface_id):
        myset = self.db.interface
        data = myset.find({"_id": interface_id}, {"method": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            data = L[0]["method"]
        else:
            data = None
        return data

    # 获取path
    def get_path(self, interface_id):
        myset = self.db.interface
        data = myset.find({"_id": interface_id}, {"path": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            data = L[0]["path"]
        else:
            data = None
        return data

    # 获取type
    def get_type(self, interface_id):
        myset = self.db.interface
        data = myset.find({"_id": interface_id}, {"req_body_type": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            data = L[0]["req_body_type"]
        else:
            data = None
        return data

    # 获取query
    def get_query(self, interface_id):
        myset = self.db.interface_case
        data = myset.find({"interface_id": interface_id}, {"req_query": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            data = L[0]["req_query"]
            D = {}
            for i in data:
                key = i["name"]
                value = i["value"]
                D[key] = value
        else:
            D = None
        return D

    # 获取json类型参数
    def get_req_body_json(self, interface_id):
        myset = self.db.interface_case
        data = myset.find({"interface_id": interface_id}, {"req_body_other": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            data = json.loads(L[0]["req_body_other"])
        else:
            data = None
        return data

    # 获取form类型参数
    def get_req_body_form(self, interface_id):
        myset = self.db.interface_case
        data = myset.find({"interface_id": interface_id}, {"req_body_form": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            data = L[0]["req_body_form"]
            D = {}
            for i in data:
                key = i['name']
                value = i['value']
                D[key] = value
            data = D
        else:
            data = None
        return data

    # 获取接口名称
    def get_interface_name(self, interface_id):
        myset = self.db.interface
        data = myset.find({"_id": int(interface_id)}, {"title": 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            title = L[0]["title"]
        else:
            title = None
        return title


# 执行脚本类
class run(SqlOperate):
    '''
    参数为任务id
    run该任务下所有接口请求
    '''

    def __init__(self, task_id):
        self.task_id = task_id
        conf = configparser.ConfigParser()
        # conf.read("/home/jinyue/test/conf/config.ini")
        conf.read("../conf/config.ini")
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
    def run_api(self, url, method, params, data, json):
        try:
            if method == "GET":
                r = requests.get(url, params=params, timeout=(10, 10))
            elif method == "POST":
                r = requests.post(url, params=params, data=data, json=json, timeout=(10, 10))
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
    def write_result(self, api_id, task_id, resq_code, res_time, response):
        response = pymysql.escape_string(response)
        create_time = int(time.time())
        self.dbcur()
        sql = self.sqlInsert("apirun_result",
                             {"api_id": api_id, "task_id": task_id, "resq_code": resq_code,
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
def main(task_id):
    task_id = int(task_id)
    r = run(task_id)
    m = get_md()
    strategy = Monitor_Inform()
    send = Send_All()
    api_list = r.get_taskinfo()[2][1:-1].split(",")
    for i in api_list:
        print(datetime.datetime.now())
        i = int(i)
        interface_name = m.get_interface_name(i)
        url = m.get_domain(i)
        if url is None:
            print("接口id：%s 不存在正式环境，跳过" % i)
            continue
        method = m.get_method(i)
        path = m.get_path(i)
        url = url + path
        query = m.get_query(i)
        if method == "POST":
            form = m.get_req_body_form(i)
            json = m.get_req_body_json(i)
        else:
            form = None
            json = None
        resq_code, res_time, response = r.run_api(url, method, query, data=form, json=json)
        if resq_code == 200:
            response = "ok"
        r.write_result(i, task_id, resq_code, res_time, response)
        print(task_id, i, resq_code, res_time)
        st = strategy.start_inform(task_id, i, resq_code)
        num = st[4]
        print(st)
        if str(resq_code)[:1]=="9":
            resq_code=str(resq_code)+"(接口响应超过10s)"
        else:
            resq_code=str(resq_code)
        if st[0] == 1:
            content = " 接口id：%d \n 接口名称：%s \n 接口地址：%s \n 状态码：%s\n 备注：%s " % (i, interface_name, url, resq_code, st[1])
            d_token = st[2]
            receiver = st[3]
            send.sending(d_token, content)
            send.sendemail(receiver, content)
        strategy.upnum(i, num)
    else:
        print("执行完成")


if __name__ == "__main__":
    task_id = sys.argv[1]
    # task_id = 9
    main(task_id)
