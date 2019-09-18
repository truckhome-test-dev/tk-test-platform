from test_code import *
import configparser
import time


class Monitor_Res(SqlOperate):
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('monitor_db', 'host')
        self.user = conf.get('monitor_db', 'user')
        self.passwd = conf.get('monitor_db', 'passwd')
        self.database = conf.get('monitor_db', 'database')

    # 获取当前时间和一周前时间
    def get_time(self):
        """
        :return: 2019-03-30 20:41:18 - 2019-05-29 20:41:18
        """
        # 获取当天23：59:59时间戳
        t = time.localtime(time.time())
        time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))

        end_time = int(time1) + 86399
        start_time = end_time - 86400 * 7 + 1
        timeArray = time.localtime(end_time)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        timeArray = time.localtime(start_time)
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        mydate = str(start_time) + ' - ' + str(end_time)
        return mydate

    #获取异常接口数据，返回绘制饼图所需数据结构
    def get_task_statistics(self,task_id,time_frame=None):
        if time_frame == None or time_frame == "":
            time_frame=self.get_time()
        data = time_frame.split(" - ")
        start_time = int(time.mktime(time.strptime(data[0], '%Y-%m-%d %H:%M:%S')))
        end_time = int(time.mktime(time.strptime(data[1], '%Y-%m-%d %H:%M:%S')))
        self.dbcur()
        sql = "select resq_code,count(*) from apirun_result where task_id=%s and create_time between %s and %s group by resq_code"%(task_id,start_time,end_time)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        L=[]
        for i in data:
            d={}
            d['name']=i[0]
            d['value']=i[1]
            L.append(d)
        return L


    #获取异常api数据
    def api_errdata(self,task_id,time_frame=None):
        if time_frame == None or time_frame == "":
            time_frame=self.get_time()
        data = time_frame.split(" - ")
        start_time = int(time.mktime(time.strptime(data[0], '%Y-%m-%d %H:%M:%S')))
        end_time = int(time.mktime(time.strptime(data[1], '%Y-%m-%d %H:%M:%S')))
        self.dbcur()
        sql = "select api_id,resq_code,count(id) from apirun_result where task_id=%s and create_time between %s and %s and resq_code != 200 group by api_id,resq_code"%(task_id,start_time,end_time)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data=self.cur.fetchall()
        return data

    #封装成echarts需要的格式
    def api_err(self,task_id,time_frame=None):
        data=self.api_errdata(task_id,time_frame=time_frame)
        print(data)
        apilist=[]
        for i in data:
            if i[0] in apilist:
                continue
            apilist.append(i[0])
        errtype=[]
        for i in data:
            if i[1] in errtype:
                continue
            errtype.append(i[1])
        #未完成，暂时未用到此方法
        print(apilist,len(apilist))
        print(errtype, len(errtype))

    #获取接口响应时间数据
    def api_rt(self,api_id,time_frame=None):
        if time_frame == None or time_frame == "":
            time_frame=self.get_time()
        data = time_frame.split(" - ")
        start_time = int(time.mktime(time.strptime(data[0], '%Y-%m-%d %H:%M:%S')))
        end_time = int(time.mktime(time.strptime(data[1], '%Y-%m-%d %H:%M:%S')))
        self.dbcur()
        sql = "select create_time,res_time from apirun_result where api_id=%s and create_time between %s and %s order by create_time asc"%(api_id,start_time,end_time)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data=self.cur.fetchall()
        L=[]
        x=[]
        y=[]
        for i in data:
            timeArray = time.localtime(i[0])
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            x.append(otherStyleTime)
            y.append(i[1])
        L.append(x)
        L.append(y)
        return L

    #获取项目名称
    def get_pro(self):
        self.dbcur()
        sql = "select name from product"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = list(self.cur.fetchall())
        return data

    #通过项目名称获取所有接口名称列表
    def get_api(self,pro_name):
        self.dbcur()
        sql = "select a.id,a.urlname from api_list as a,product as p where a.pro_id = p.ID and p.name='%s'"%pro_name
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = list(self.cur.fetchall())
        L=[]
        for i in data:
            a=list(i)
            L.append(a)
        return L
