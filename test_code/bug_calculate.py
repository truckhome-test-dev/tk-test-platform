import configparser
import time
from test_code.sqlop import *


class Bug_Calculate(SqlOperate):
    # 连接数据库
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.host = conf.get('qa', 'host')
        self.user = conf.get('qa', 'user')
        self.passwd = conf.get('qa', 'passwd')
        self.database = conf.get('qa', 'database')

    # 插入数据
    def insData(self, tablename, field_item):
        self.dbcur()
        sql = self.sqlInsert(tablename, field_item)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()

    # 插入质量数据
    def bugInsert(self, vname, proname, versionname, name, checknum, fristnum, leaknum, newnum, bugcount, bugdensity,
                  fristleak, bringerror, addtime):
        data1 = self.selbugcalculate(vname,proname,versionname)
        self.dbcur()
        sql = ""
        if data1:
            #self.delbugcalculate(vname,proname,versionname)
            #sql ="INSERT INTO bugcalculate (vname,proname,versionname,name,checknum,fristnum,leaknum,newnum,bugcount,bugdensity,fristleak,bringerror,addtime)VALUES( '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(vname,proname,versionname,name,checknum,fristnum,leaknum,newnum,bugcount,bugdensity,fristleak,bringerror,addtime)
            sql = "update bugcalculate SET name ='%s',checknum='%s',fristnum='%s',leaknum='%s',newnum='%s',bugcount='%s',bugdensity='%s',fristleak='%s',bringerror='%s',addtime='%s' where vname ='%s'and proname='%s' and versionname='%s'" %(name,checknum,fristnum,leaknum,newnum,bugcount,bugdensity,fristleak,bringerror,addtime,vname,proname,versionname)
        else:
            # self.insData('bugcalculate', {'vname': vname, 'proname': proname, 'versionname': versionname, 'name': name,
            #                               'checknum': checknum, 'fristnum': fristnum, 'leaknum': leaknum, 'newnum': newnum,
            #                               'bugcount': bugcount, 'bugdensity': bugdensity, 'fristleak': fristleak,
            #                               'bringerror': bringerror, 'addtime': addtime})
            sql ="INSERT INTO bugcalculate (vname,proname,versionname,name,checknum,fristnum,leaknum,newnum,bugcount,bugdensity,fristleak,bringerror,addtime)VALUES( '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(vname,proname,versionname,name,checknum,fristnum,leaknum,newnum,bugcount,bugdensity,fristleak,bringerror,addtime)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.bugnewsel()
        if data:
            self.bugdel()
        else:
            self.bugnewinser()
        return "pass"

    #查询新增bug率数据是否存在
    def selbugcalculate(self,vname,proname,versionname):
        self.dbcur()
        sql = "select vname,proname,versionname from bugcalculate where vname ='%s' and proname ='%s' and versionname ='%s' "%(vname,proname,versionname)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

    #删除某条bug数据
    # def delbugcalculate(self,vname,proname,versionname):
    #     self.dbcur()
    #     sql = "delete from buproname,gcalculate where vname ='%s'AND proname='%s' AND versionname='%s'" %(vname,proname,versionname)
    #     self.sqlExe(sql)
    #     self.sqlCom()
    #     self.sqlclo()
    #     return "pass"

    #查询bug密度、首轮漏测率、引入错误率
    def getInfor(self,vname,proname,versionname):
        self.dbcur()
        #sql = "select bugdensity,fristleak,bringerror from bugcalculate order by id desc limit 1"
        sql = "select bugdensity,fristleak,bringerror from bugcalculate where vname ='%s'AND proname='%s' AND versionname='%s'" %(vname,proname,versionname)
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data=self.cur.fetchone()
        return data

    # 查询质量数据
    def getInfor1(self):
        self.dbcur()
        sql = "select * from bugcalculate order by addtime desc limit 30"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

    # 查询bug率数据
    def bugselect(self):
        self.dbcur()
        sql = "select * from bugmidu"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

    # 判断是否有本月bug率数据
    def bugnewsel(self):
        self.dbcur()
        sql = "select * from bugmidu WHERE addtime= DATE_FORMAT(CURDATE(),'%Y-%m')"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data

    # 新增本月bug率
    def bugnewinser(self):
        self.dbcur()
        sql = "insert into bugmidu(addtime,density,leakage,lead,updatetime)select DATE_FORMAT( addtime, '%Y-%m' ),ROUND(sum(bugdensity)/count(proname),2),ROUND(sum(fristleak)/count(proname),2),ROUND(sum(bringerror)/count(proname),2),CURDATE( ) from bugcalculate WHERE DATE_FORMAT( addtime, '%Y-%m' ) = DATE_FORMAT( CURDATE( ) , '%Y-%m' )  group by DATE_FORMAT(addtime,'%Y-%m')"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        return "pass"

    # 查询本月质量数据
    def buginsert(self):
        self.dbcur()
        sql = "select ROUND(sum(bugdensity)/count(proname),2),ROUND(sum(fristleak)/count(proname),2),ROUND(sum(bringerror)/count(proname),2) from bugcalculate WHERE DATE_FORMAT( addtime, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )  group by DATE_FORMAT(addtime,'%Y%m')"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchone()
        return data

    # 更新bug率本月数据
    def bugdel(self):
        data = self.buginsert()
        self.dbcur()
        sql = "update bugmidu SET `density`=%.2f, `leakage`=%.2f, `lead`=%.2f,`updatetime`='%s' WHERE addtime='%s'" % (
        data[0], data[1], data[2], time.strftime('%Y-%m-%d', time.localtime(time.time())),
        time.strftime('%Y-%m', time.localtime(time.time())))
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        return "pass"

    # 更新bug率本月数据
    def countbug(self):
        self.dbcur()
        sql = "select ROUND(sum(bugdensity)/count(proname),2),ROUND(sum(fristleak)/count(proname),2),ROUND(sum(bringerror)/count(proname),2) from bugcalculate where date_format(addtime,'%Y-%m') < date_format(CURDATE( ),'%Y-%m')"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        l = []
        for i in data:
            l.append(i[0])
            l.append(i[1])
            l.append(i[2])
        return l

    # 查询出周数据
    def weekcount(self):
        self.dbcur()
        sql = "SELECT id,vname,proname,versionname,checknum,fristnum,leaknum,newnum,bugcount,bugdensity,fristleak,bringerror,addtime FROM bugcalculate  WHERE YEARWEEK(date_format(addtime,'%Y-%m-%d')) = YEARWEEK(now())"
        self.sqlExe(sql)
        self.sqlCom()
        self.sqlclo()
        data = self.cur.fetchall()
        return data
