from functools import wraps
import json
from flask import session, Flask, request, render_template, redirect, url_for, flash, Response
from test_code.sqlop import *


# 校验权限
def permissions(level, function):
    conf = configparser.ConfigParser()
    conf.read("conf/config.ini")
    db_qa = pymysql.connect(conf.get('qa', 'host'), conf.get('qa', 'user'), conf.get('qa', 'passwd'),
                            conf.get('qa', 'database'), charset='utf8')
    cur = db_qa.cursor()
    sql = "select * from permissions,`function` where permissions.function_id=`function`.id and permissions.`level`=%s and value='%s'" % (
        level, function)
    cur.execute(sql)
    db_qa.commit()
    db_qa.close()
    data = cur.fetchone()
    if not data:
        return False
    else:
        return True


# 判断是否有权限装饰器
def check_permissions(function):
    """
    放在需要校验登录或者权限的方法前
    :param function: 方法名
    :return: 如果未登录返回
                get请求重定向到登录
                post请求{"code": 1001, "mes": "未登录"}
            有权限直接执行对应的方法
            无权限返回{"code": 1001,"mes":"无权限"}
    """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            leven = session.get('username')
            if leven is None:
                if request.method == 'GET':
                    data=redirect('/login_new')
                else:
                    data = json.dumps({"code": 1001, "mes": "未登录"})
                return data
            else:
                if not permissions(leven[1], function):
                    data = json.dumps({"code": 1002, "mes": "无权限"})
                    return data
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper


#获取菜单目录
def get_menu(level):
    """
    :param level: 角色等级
    :return: 字典格式的菜单目录
    """
    conf = configparser.ConfigParser()
    conf.read("conf/config.ini")
    db_qa = pymysql.connect(conf.get('qa', 'host'), conf.get('qa', 'user'), conf.get('qa', 'passwd'),
                            conf.get('qa', 'database'), charset='utf8')
    cur = db_qa.cursor()
    sql = "select f.id,f.name,f.value,f.father_id,f.sort " \
          "from `function` as f,permissions as p " \
          "where f.id=p.function_id and p.`level`=%s"%level
    cur.execute(sql)
    db_qa.commit()
    db_qa.close()
    data = cur.fetchall()
    l = []
    d = {}
    for i in data:
        if i[3] == 0:
            l.append([i[0],i[1],i[4]])
            l.sort(key=lambda x: x[2])
    for y in l:
        d3 = {}
        l1=[]
        for i in data:
            if i[3] == y[0]:
                l2=[i[1],i[2],i[4]]
                l1.append(l2)
                l1.sort(key=lambda x: x[2])
        for j in l1:
            key = y[1]
            d3[j[0]]=j[1]
            value=d3
            d[key]=value
    return d
get_menu(70)