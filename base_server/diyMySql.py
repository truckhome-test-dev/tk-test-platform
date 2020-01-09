#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2019/12/14 13:33
# @Author  : Mr. Cui
# @File    : diyMySql.py
# @Software: PyCharm
import traceback
import pymysql
#from server import log

#Log = log.Logger('dberr.log')


class DataBaseHandle(object):
    ''' 定义一个 MySQL 操作类'''

    def __init__(self, host, username, password, database, port):
        '''初始化数据库信息并创建数据库连接'''
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port, charset='utf8')

     # 这里 注释连接的方法，是为了 实例化对象时，就创建连接。不许要单独处理连接了。
    def connDataBase(self):
        ''' 数据库连接 '''

        self.db = pymysql.connect(self.host,self.username,self.password,self.database,self.port,charset='utf8')

        # self.cursor = self.db.cursor()

        return self.db

    def insertDB(self, sql, args=None):
        ''' 插入数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            # self.cursor.execute(sql,args)
            ret = self.cursor.execute(sql, args)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            ret = [1, ret]
            # print(ret)
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            self.db.rollback()
            ret = [0, str(e)]
            #Log.logger.error(traceback.format_exc())
        finally:
            self.cursor.close()
        return ret

    def deleteDB(self, sql, args=None):
        ''' 操作数据库数据删除 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            # self.cursor.execute(sql,args)
            ret = self.cursor.execute(sql, args)  # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            ret = [1, ret]
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            self.db.rollback()
            ret = [0, str(e)]
            #Log.logger.error(traceback.format_exc())
        finally:
            self.cursor.close()
        return ret

    def updateDb(self, sql, args=None):
        ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql, args)
            ret = self.cursor.execute(sql, args)  # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            ret = [1, ret]
            # print(tt)
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            self.db.rollback()
            ret = [0, str(e)]
            #Log.logger.error(traceback.format_exc())
        finally:
            self.cursor.close()
        return ret

    def selectDb(self, sql, args=None):
        ''' 数据库查询 '''
        #print(111)
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql, args)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            data = self.cursor.fetchall()  # 返回所有记录列表
            ret = [1, data]
            #Log.logger.error(ret)
        except Exception as e:
            ret = [0, str(e)]
            #Log.logger.error(traceback.format_exc())
        finally:
            self.cursor.close()
        return ret

    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.db.close()


if __name__ == '__main__':
    DbHandle = DataBaseHandle('103.45.112.121', 'xiequ', 'HMKDhBHfr8Fr2Jn3', 'xiequ', 3306)

    print(DbHandle.insertDB('insert into `user` values (%s,%s,%s,%s,%s,%s,%s)',
                            (2, 'FuHongXue --', 'FuHongXue', 'FuHongXue', 'FuHongXue', 'FuHongXue', 'FuHongXue')))
