from test_code.sqlop import *
# from sqlop import *
import configparser
import time
import datetime


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
    def task_add(self, task_name, api_id, frequency):
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
                              "create_time": create_time, "update_time": create_time})
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
        sql = self.sqlSelect("task_list", ["id", "task_name", "api_id", "frequency", "status"],
                             condition={"is_delete": 0}, repeat="1")
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
        sql = "select id,task_name,api_id,frequency,status from task_list where id='%s'" % task_id
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        data = list(data)
        data[2] = data[2][1:-1]
        return data

    # 编辑任务
    def task_edit(self, task_id, task_name, api_id, frequency):
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
                                           "update_time": update_time},
                             {"id": task_id})
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
        #SQL查询
        sql = "select res.id,task.task_name,api.urlname,api.url,api.method,api.parameters_data,res.resq_code,res.res_time,res.response,res.create_time " \
              "from apirun_result as res,api_list as api,task_list as task " \
              "where res.api_id = api.id and res.task_id = task.id"
        #根据参数进行判断，拼接SQL
        if time_frame != None and time_frame != "":
            data = time_frame.split(" - ")
            start_time = int(time.mktime(time.strptime(data[0], '%Y-%m-%d %H:%M:%S')))
            end_time = int(time.mktime(time.strptime(data[1], '%Y-%m-%d %H:%M:%S')))
            sql += " and res.create_time between %s and %s" % (str(start_time), str(end_time))
        elif task_id != None and task_id != ""and task_id !="undefined":
            sql += " and res.task_id=%s" % task_id
        elif api_id != None and api_id != ""and api_id !="undefined":
            sql += " and res.api_id=%s" % api_id
        elif res_id != None and res_id != "" and res_id !="undefined":
            sql += " and res.id=%s" % res_id
        elif resq_code != None and resq_code != ""and resq_code !="undefined":
            sql += " and resq_code=%s" % resq_code
        else:
            sql += " order by res.id desc"
            if page == 0 and page != "" and page !="undefined":
                sql += " limit 200"
            else:
                sql += " limit %s,20" % str((int(page) * 20))
        #执行SQL的查询获取数据
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        data = list(data)
        data1 = []
        #时间戳
        for i in data:
            i = list(i)
            i[9] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[9]))
            data1.append(i)
        return data1

#查询总数,查询sql中表的总数
    def get_count(self):
        self.dbcur ()
        sql="select count(*) from apirun_result"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data[0]






# if __name__ == "__main__":
#     a = Monitor_Task()
#     print(a.get_rest(page=1))
