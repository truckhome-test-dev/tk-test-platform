from test_code import *
import time
import datetime
import configparser

class Grab_Bug(SqlOperate):
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('qa', 'host')
        self.user = conf.get('qa', 'user')
        self.passwd = conf.get('qa', 'passwd')
        self.database = conf.get('qa', 'database')

    #获取bug严重程度权重值
    def get_integral(self,severity):
        """
        :param severity: bug严重程度
        :return: (0,)
        """
        self.dbcur()
        sql = "select coefficient from integral where severity=%s"%severity
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data

    #计算bug积分
    def get_bug_score(self):
        bug=Mantis_Bug()
        data=bug.get_severity_count('1557997200','1558000800')
        d={}
        d1={}
        for i in data:
            if i[0] in d.keys():
                d[i[0]] = d[i[0]]+self.get_integral(i[1])[0]*i[2]
                d1[i[0]] =d1[i[0]]+i[2]
            else:
                d[i[0]] = self.get_integral(i[1])[0] * i[2]
                d1[i[0]] = i[2]
        name=[]
        score=[]
        count=[]
        for key,value in d.items():
            name.append(key)
            score.append(value)
        for key,value in d1.items():
            count.append(value)
        L=[]
        for i in range(len(name)):
            L1=[]
            L1.append(name[i])
            L1.append(count[i])
            L1.append(score[i])
            L.append(L1)
        L.sort(key=lambda x:float(x[2]),reverse=True)
        for i in range(len(L)):
            L[i].append(i+1)
        return L
