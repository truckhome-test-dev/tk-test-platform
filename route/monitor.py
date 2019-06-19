#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect
from test_code import *
from functools import wraps
import json

# 创建蓝图对象
monitor = Blueprint('monitor', __name__)
task = Monitor_Task()
api = Api_Monitor()
res = Monitor_Res()


# 判断登录装饰器方法
def check_token2(func):
    @wraps(func)
    def inner(*args, **kwargs):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        token_key = conf.get('token', 'key')
        token = request.cookies.get('token')
        if token == token_key:
            return func(*args, **kwargs)
        else:
            data = json.dumps({"code": 1001})
            return data

    return inner


# 任务列表展示
@monitor.route('/task_list', methods=['get', 'post'])
def task_list():
    if request.method == "GET":
        task_list = task.task_list()
        return render_template('task.html', task_list=task_list)


# 编辑任务
@monitor.route('/task_edit', methods=['get', 'post'])
#@check_token2
def task_edit():
    if request.method == "GET":
        title = "编辑任务"
        task_id = request.args.to_dict().get('task_id', "")
        task_info = task.task_info(task_id)
        api = "task_edit"
        return render_template('task_edit.html', api=api, title=title, task_info=task_info)
    else:
        task_id = request.form.get('task_id')
        task_name = request.form.get('task_name')
        frequency = request.form.get('frequency')
        api_id = "[" + request.form.get('api_id') + "]"
        task.task_edit(task_id, task_name, api_id, frequency)
        return redirect("http://127.0.0.1:5000/monitor/task_list")


# 添加任务
@monitor.route('/task_add', methods=['get', 'post'])
@check_token2
def task_add():
    if request.method == "GET":
        title = "添加任务"
        task_info = ("", "", "", "3", "")
        api = "task_add"
        return render_template('task_edit.html', api=api, title=title, task_info=task_info)
    else:
        task_name = request.form.get('task_name')
        frequency = request.form.get('frequency')
        api_id = "[" + request.form.get('api_id') + "]"
        task.task_add(task_name, api_id, frequency)
        # task_list = task.task_list()
        return redirect("http://127.0.0.1:5000/monitor/task_list")


# 删除任务
@monitor.route('/task_del', methods=['get', 'post'])
@check_token2
def task_del():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        task_id = data['task_id']
        ret = task.task_del(task_id)
        if ret == 'del task success':
            return 'ok'
        else:
            return ret


# 启动、停止任务
@monitor.route('/task_status', methods=['get', 'post'])
@check_token2
def task_status():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        task_id = data['task_id']
        ret = task.run(task_id)
        return ret


# 监控平台接口新增
@monitor.route('/newapi', methods=['post', 'get'])
@check_token2
def newapi():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        product = data['product']
        urlname = data['urlname']
        url = data['url']
        method = data['method']
        parm = data['parameters_json']
        # check_point = data['check_point']
        api.addapi(product, urlname, url, method, parm, check_point=0)
        return "ok"
    else:
        prolist = api.prolist()
        return render_template('apilist.html', prolist=prolist)


# 监控平台展示接口列表
@monitor.route('/apilist', methods=['post', 'get'])
def showapi():
    if request.method == 'GET':
        apidatas = api.getapi()
        prolist = api.prolist()
        count = len(api.getapi(page=-1))
        return render_template('apilist.html', apidata2=apidatas, prolist=prolist, count=count,proid=0)
    else:
        proid = request.form.get('proid')
        if proid != None:
            prolist = api.prolist()
            apidatas = api.proapi(proid, page=0)
            count = len(api.proapi(proid, count=1))
            return render_template('apilist.html', apidata2=apidatas, prolist=prolist, proid=proid,count=count)
        else:
            page = request.get_data()
            page = json.loads(page.decode("utf-8"))
            page = page['page']
            proid = request.get_data()
            proid = json.loads(proid.decode("utf-8"))
            proid = proid['proid']
            apidatas = api.proapi(proid,page=page)
            prolist = api.prolist()
            count = len(api.proapi(proid,count=1))
            return render_template('apipage.html', apidata2=apidatas, prolist=prolist, count=count)


# 监控平台修改接口内容
@monitor.route('/api', methods=['post', 'get'])
#@check_token2
def editapi():
    if request.method == 'GET':
        prolist = api.prolist()
        apiid = request.args.to_dict().get('apiid', "")
        apidata = api.getapi(apiid)
        return render_template('apiedit.html', prolist=prolist, apidata=apidata)
    else:
        urlname = request.form.get('urlname')
        url = request.form.get('url')
        method = request.form.get('method')
        parm = request.form.get('parameters_json')
        product = request.form.get('proid')
        # check_point = data['check_point']
        apiid = request.form.get('apiid')
        api.editapi(url, urlname, product, method, apiid, parm)
        return redirect("http://127.0.0.1:5000/monitor/apilist")


# 监控平台筛选项目接口
@monitor.route('/selapi', methods=['post', 'get'])
def selapi():
    if request.method == 'POST':
        proid = request.form.get('proid')
        product = api.proname(proid)
        prolist = api.prolist()
        apidatas = api.proapi(proid)
        count = len(apidatas)
        return render_template('apilist.html', apidata2=apidatas, prolist=prolist, product=product, proid=proid,
                               count=count)


# 监控平台修改接口使用状态
@monitor.route('/editstatus', methods=['post', 'get'])
@check_token2
def editapi2():
    data = request.get_data()
    data = json.loads(data)
    apiid = data['apiid']
    api.apist(apiid)
    return "ok"


# 监控平台修改接口显示状态
@monitor.route('/apishow', methods=['post', 'get'])
@check_token2
def editapi3():
    data = request.get_data()
    data = json.loads(data)
    apiid = data['apiid']
    api.apishows(apiid)
    return "ok"


# 查询结果
@monitor.route('/report', methods=['get', 'post'])
def report():
    if request.method == "GET":
        task_id = request.args.to_dict().get('task_id', "") #根据数据类型进行转换
        res = task.get_rest(task_id=task_id)
        count = len(api.getapi(page=-1))
        return render_template('report.html', res=res, time_frame="", task_id=task_id, api_id="", res_id="",
                               resq_code="",count=count)
    else:
        test10 = request.form.get('test10')
        if test10 != None:
            prolist = api.prolist()
            apidatas = api.proapi(test10, page=0)
            count = len(api.proapi(test10, count=1))
            return render_template('report.html', apidata2=apidatas, prolist=prolist, test10=test10, count=count)
        else:
            page = request.get_data()#获取页数的编号
            page = json.loads(page.decode("utf-8"))#json.loads函数的使用
            page = page['page']#页面=页面的page
            test10 = request.get_data()
            test10 = json.loads(test10.decode("utf-8"))
            test10 = test10['test10']
            apidatas = api.proapi(test10, page=page)
            prolist = api.prolist()
            count = len(api.proapi(test10, count=1))
            return render_template('report.html', apidata2=apidatas, prolist=prolist, count=count)

            if request.method == "POST":
                time_frame = request.form.get('time_frame')
                task_id = request.form.get('task_id')
                api_id = request.form.get('api_id')
                res_id = request.form.get('res_id')
                resq_code = request.form.get('resq_code')
                res = task.get_rest(time_frame=time_frame, task_id=task_id, api_id=api_id, res_id=res_id, resq_code=resq_code)
                return render_template('report.html', res=res, time_frame=time_frame, task_id=task_id, api_id=api_id,
                                       res_id=res_id, resq_code=resq_code)

# 验证token
@monitor.route('/token_check', methods=['post', 'get'])
def token_check():
    if request.method == 'POST':
        global token
        token = request.get_data()

        if token == b'':
            token = request.cookies.get('token')
        else:
            token = json.loads(token.decode("utf-8"))
            token = str(token['token'])
        data = token_check1(token)
        return json.dumps(data)
    else:
        return render_template('admin.html')

@monitor.route('/result', methods=['get', 'post'])
def result():
    tasklist = task.task_list()
    prolist= res.get_pro()
    if request.method == 'GET':
        mydate=res.get_time()
        return render_template('result.html',tasklist=tasklist,prolist=prolist,mydate=mydate)
    else:
        task_id = request.get_data()
        task_id = json.loads(task_id.decode("utf-8"))
        task_id = task_id['task_id']
        time_frame= request.get_data()
        time_frame = json.loads(time_frame.decode("utf-8"))
        time_frame = time_frame['time_frame']

        taskstatis = res.get_task_statistics(task_id,time_frame=time_frame)
        data = {"code": 1000, "taskstatis": taskstatis}
        return json.dumps(data)

@monitor.route('/apistatis', methods=['get', 'post'])
def apistatis():
    if request.method == 'POST':
        api_id = request.get_data()
        api_id = json.loads(api_id.decode("utf-8"))
        api_id = api_id['api_id']

        time_frame = request.get_data()
        time_frame = json.loads(time_frame.decode("utf-8"))
        time_frame = time_frame['time_frame']
        rt=res.api_rt(api_id,time_frame=time_frame)
        data={"code": 1000,"t":rt[0],"r":rt[1]}
        return json.dumps(data)

@monitor.route('/get_apiname', methods=['get', 'post'])
def get_apiname():
    if request.method == 'POST':
        pro_name = request.get_data()
        pro_name = json.loads(pro_name.decode("utf-8"))
        pro_name = pro_name['pro_name']

        api_name=res.get_api(pro_name)
        if api_name:
            data = {"code": 1000,"api_name": api_name}
        else:
            data = {"code": 1002,"api_name": api_name}
        return json.dumps(data)



