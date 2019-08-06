from test_code.sqlop import *
# from sqlop import *
import configparser
import time
import datetime
import pymongo
import json


class Monitor_Task(SqlOperate):
    '''
    任务相关方法
    '''

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('monitor_db', 'host')
        self.user = conf.get('monitor_db', 'user')
        self.passwd = conf.get('monitor_db', 'passwd')
        self.database = conf.get('monitor_db', 'database')

    # 添加任务
    def task_add(self, task_name, api_id, frequency,start_inform,token,re_email,stop_inform,re_inform,inform):
        '''
        :param task_name:
        :param api_id:列表
        :param frequency:
        :return:
        '''
        create_time = int(time.time())
        self.dbcur()
        sql = self.sqlInsert("task_list",
                             {"task_name": task_name, "api_id": api_id, "frequency": frequency,
                              "create_time": create_time, "update_time": create_time,"start_inform":start_inform,
                              "token":token,"re_email":re_email,"stop_inform":stop_inform,"re_inform":re_inform,"inform":inform})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret = "add task success"
        except pymysql.err.IntegrityError as e:
            ret = e
        return ret

    # 任务列表
    def task_list(self):
        '''
        不需要参数
        :return: (('APP', None, '', 0), ('产品库', None, '', 0), ('互动', None, '60s', 0)）
        '''
        self.dbcur()
        sql = self.sqlSelect("task_list", ["id", "task_name", "api_id", "frequency", "status","start_inform","token"
            ,"re_email","stop_inform","re_inform","inform"],condition={"is_delete": 0}, repeat="1")
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

    # 任务详情
    def task_info(self, task_id):
        '''
        :param task_id:
        :return: (1,'论坛', '[1,32,34]', '20',1)/不存在返回None
        '''
        self.dbcur()
        sql = "select id,task_name,api_id,frequency,status,start_inform,token,re_email,stop_inform,re_inform,inform from task_list where id='%s'" % task_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        data = list(data)
        data[2] = data[2][1:-1]
        return data

    # 编辑任务
    def task_edit(self, task_id, task_name, api_id, frequency,start_inform,token,re_email,stop_inform,re_inform,inform):
        '''
        :param id:
        :param task_name:
        :param api_id:
        :param frequency:
        :return:
        '''
        update_time = int(time.time())
        data = self.task_info(task_id)
        if data is None:
            return "任务id不存在"
        self.dbcur()
        sql = self.sqlUpdate("task_list", {"task_name": task_name, "api_id": api_id, "frequency": frequency,
                                           "update_time": update_time,"start_inform":start_inform,"token":token,"re_email":re_email,"stop_inform":stop_inform,"re_inform":re_inform,"inform":inform},{"id": task_id})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret = "edit task success"
        except pymysql.err.IntegrityError as e:
            ret = e
        return ret

    # 修改任务状态
    def task_status(self, task_id, status):
        '''
        :param task_id:
        :return:
        '''
        data = self.task_info(task_id)
        if data is None:
            return "任务id不存在"
        self.dbcur()
        sql = self.sqlUpdate("task_list", {"status": status}, {"id": task_id})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret = "edit task status success"
        except pymysql.err.IntegrityError as e:
            ret = e
        return ret

    # 删除任务
    def task_del(self, task_id):
        '''
        :param task_id:
        :return:
        '''

        data = self.task_info(task_id)
        if data is None:
            return "任务id不存在"
        self.dbcur()
        sql = self.sqlUpdate("task_list", {"is_delete": 1}, {"id": task_id})
        try:
            self.sqlExe(sql)
            self.sqlCom()
            self.sqlclo()
            ret = "del task success"
        except pymysql.err.IntegrityError as e:
            ret = e
        return ret

    # 删除定时任务
    def timingtask_del(self, task_id):
        '''
        :param task_id:
        :return:
        '''
        data = "monitor_run.py %d" % task_id
        with open("/var/spool/cron/root", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("/var/spool/cron/root", "w", encoding="utf-8") as f_w:
            for line in lines:
                if data in line:
                    continue
                f_w.write(line)

    # 添加定时任务
    def timingtask_add(self, task_id):
        '''
        :param task_id:
        :param frequency:
        :return:"task_id已存在"/"添加定时任务成功"
        */10 * * * * /usr/sbin/ntpdate ntp3.aliyun.com
        #* * * * * /root/.pyenv/shims/python /home/jinyue/tk-test-platform/test_code/monitor_run.py 1 >> /home/jinyue/tk-test-platform/test_code/load.log
        '''
        frequency = int(self.task_info(task_id)[3])
        if frequency == 1:
            data = "* * * * * /root/.pyenv/shims/python /home/jinyue/test/test_code/monitor_run.py %d >> /home/jinyue/test/test_code/task.log\n" % task_id
        else:
            data = "*/%d * * * * /root/.pyenv/shims/python /home/jinyue/test/test_code/monitor_run.py %d >> /home/jinyue/test/test_code/task.log\n" % (
                frequency, task_id)
        data_task = "monitor_run.py %d" % task_id
        with open("/var/spool/cron/root", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("/var/spool/cron/root", "a", encoding="utf-8") as f_w:
            for line in lines:
                if data_task in line:
                    ret = "task_id已存在"
                    break
            else:
                f_w.write(data)
                ret = "添加定时任务成功"
            return ret

    # 启动停止任务
    def run(self, task_id):
        '''
        :param task_id:
        :return:1->0/ 0->1
        '''
        status = self.task_info(task_id)[4]
        if status is None:
            return "任务id不存在"
        elif status == 1:
            self.task_status(task_id, 0)
            self.timingtask_del(task_id)
        elif status == 0:
            self.task_status(task_id, 1)
            self.timingtask_add(task_id)
        return "ok"

    # 执行结果查询
    """这块逻辑看不懂，脑袋疼"""

    def get_rest(self, time_frame=None, task_id=None, api_id=None, res_id=None, resq_code=None, page=0):
        self.dbcur()
        sql = "select res.id,task.task_name,api.urlname,api.url,api.method,api.parameters_data,res.resq_code,res.res_time,res.response,res.create_time " \
              "from apirun_result as res,api_list as api,task_list as task " \
              "where res.api_id = api.id and res.task_id = task.id"
        if time_frame != None and time_frame != "":
            data = time_frame.split(" - ")
            start_time = int(time.mktime(time.strptime(data[0], '%Y-%m-%d %H:%M:%S')))
            end_time = int(time.mktime(time.strptime(data[1], '%Y-%m-%d %H:%M:%S')))
            sql += " and res.create_time between %s and %s" % (str(start_time), str(end_time))

        elif task_id != None and task_id != "" and task_id != "undefined":
            sql += " and res.task_id=%s" % task_id
        elif api_id != None and api_id != "" and api_id != "undefined":
            sql += " and res.api_id=%s" % api_id
        elif res_id != None and res_id != "" and res_id != "undefined":
            sql += " and res.id=%s" % res_id
        elif resq_code != None and resq_code != "" and resq_code != "undefined":
            sql += " and resq_code=%s" % resq_code
        else:
            sql += " order by res.id desc"
            if page == 0 and page != "" and page != "undefined":
                sql += " limit 100"
            else:
                sql += " limit %s,20" % str((int(page) * 20))
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        data = list(data)
        data1 = []
        for i in data:
            i = list(i)
            i[9] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[9]))
            data1.append(i)
        return data1

    # 查询总数,查询sql中表的总数
    def get_count(self):
        self.dbcur()
        sql = "select count(*) from apirun_result"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data[0]


class Monitor_Mongodb():
    def __init__(self):
        self.conn = pymongo.MongoClient('192.168.2.1', 27017)
        self.db = self.conn.yapi

    # 获取所有分组
    def get_group(self):
        myset = self.db.group
        # data = myset.find({'type': 'public'}, {'group_name': 1})
        data = myset.aggregate([{"$match": {"type": "public"}}, {"$project": {"_id": 0, "id": "$_id", "title": "$group_name"}}])
        L = []
        for i in data:
            L.append(i)
        return L

    # 获取某分组下项目
    def get_project(self, group_id):
        myset = self.db.project
        # data = myset.find({'group_id': int(group_id)}, {'name': 1})
        data = myset.aggregate([{"$match": {"group_id": group_id}}, {"$project": {"_id": 0, "id": "$_id", "title": "$name"}}])
        L = []
        for i in data:
            L.append(i)
        return L

    # 获取某项目下模块
    def get_interface_cat(self, project_id):
        myset = self.db.interface_cat
        # data = myset.find({'project_id': int(project_id)}, {'name': 1})
        data = myset.aggregate([{"$match": {"project_id": project_id}}, {"$project": {"_id": 0, "id": "$_id", "title": "$name"}}])
        L = []
        for i in data:
            L.append(i)
        return L

    # 判断接口是否创建了测试用例
    def has_case(self, interface_id):
        myset = self.db.interface_case
        data = myset.find({'interface_id': int(interface_id)}, {'name': 1})
        L = []
        for i in data:
            L.append(i)
        return L

    # 获取某模块下接口
    def get_interface(self, catid):
        myset = self.db.interface
        # data = myset.find({'catid': int(catid)}, {'title': 1})
        data = myset.aggregate([{"$match": {"catid": catid}}, {"$project": {"_id": 0, "id": "$_id", "title": "$title"}}])
        L = []
        for i in data:
            L.append(i)
        return L

    # 获取项目下所有接口id
    def get_allinterface(self, project_id):
        myset = self.db.interface
        data = myset.find({'project_id': int(project_id)}, {'__id': 1})
        L = []
        for i in data:
            L.append(i)
        if L != []:
            l1 = []
            for i in L:
                i_id = i["_id"]
                l1.append(i_id)
        else:
            l1 = []
        return l1

if __name__ == "__main__":
    a = Monitor_Mongodb()
    print(a.get_group())
#     L=[]
#     for i in [376,370,364,358,352,346,340,334,328,322,316,310,304,298,292,286,280,274,268,262,256,250,244,232]:
#         print(i)
#         q=a.get_allinterface(i)
#         print(q)
#         L+=q
#     print(L)
