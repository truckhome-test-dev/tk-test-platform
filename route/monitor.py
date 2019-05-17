#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect
from test_code import *

# 创建蓝图对象
monitor = Blueprint('monitor', __name__)
task = Monitor_Task()
api = Api_Monitor()

# 任务列表展示
@monitor.route('/task_list', methods=['get', 'post'])
def task_list():
    if request.method == "GET":
        task_list = task.task_list()
        return render_template('task.html', task_list=task_list)


# 编辑任务
@monitor.route('/task_edit', methods=['get', 'post'])
def task_edit():
    if request.method == "GET":
        title = "编辑任务"
        task_id = request.args.to_dict().get('task_id', "")
        task_info = task.task_info(task_id)
        api = "task_edit"
        return render_template('task_edit.html', api=api,title=title, task_info=task_info)
    else:
        task_id = request.form.get('task_id')
        task_name = request.form.get('task_name')
        frequency = request.form.get('frequency')
        api_id = "[" + request.form.get('api_id') + "]"
        task.task_edit(task_id,task_name, api_id, frequency)
        return redirect("http://127.0.0.1:5000/monitor/task_list")


# 添加任务
@monitor.route('/task_add', methods=['get', 'post'])
def task_add():
    if request.method == "GET":
        title = "添加任务"
        task_info = ("","", "", "3", "")
        api="task_add"
        return render_template('task_edit.html', api=api,title=title, task_info=task_info)
    else:
        task_name = request.form.get('task_name')
        frequency = request.form.get('frequency')
        api_id = "[" + request.form.get('api_id') + "]"
        task.task_add(task_name, api_id, frequency)
        # task_list = task.task_list()
        return redirect("http://127.0.0.1:5000/monitor/task_list")

# 删除任务
@monitor.route('/task_del', methods=['get', 'post'])
def task_del():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        task_id = data['task_id']
        ret=task.task_del(task_id)
        if ret=='del task success':
            return 'ok'
        else:
            return ret

#启动、停止任务
@monitor.route('/task_status', methods=['get', 'post'])
def task_status():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        task_id = data['task_id']
        ret=task.run(task_id)
        return ret


#监控平台接口新增
@monitor.route('/newapi',methods=['post','get'])
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
        api.addapi(product,urlname,url,method,parm,check_point=0)
        return "ok"
    else:
        prolist = api.prolist()
        return render_template('apilist.html',prolist=prolist)

#监控平台展示接口列表
@monitor.route('/apilist',methods=['post','get'])
def showapi():
    if request.method == 'GET':
        apidatas = api.getapi()
        prolist = api.prolist()
        return render_template('apilist.html',apidata2=apidatas,prolist=prolist)

#监控平台修改接口内容
@monitor.route('/api',methods=['post','get'])
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
        api.editapi(url,urlname,product,method,apiid,parm)
        return redirect("http://127.0.0.1:5000/monitor/apilist")

#监控平台筛选项目接口
@monitor.route('/selapi',methods=['post','get'])
def selapi():
    if request.method == 'POST':
        proid = request.form.get('proid')
        product = api.proname(proid)
        prolist = api.prolist()
        apidatas = api.proapi(proid)
        return render_template('apilist.html',apidata2=apidatas,prolist=prolist,product=product,proid=proid)

#监控平台修改接口使用状态
@monitor.route('/editstatus',methods=['post','get'])
def editapi2():
    data = request.get_data()
    data = json.loads(data)
    apiid = data['apiid']
    api.apist(apiid)
    return "ok"

#监控平台修改接口显示状态
@monitor.route('/apishow',methods=['post','get'])
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
        task_id = request.args.to_dict().get('task_id', "")
        res = task.get_rest(task_id=task_id)
        return render_template('report.html', res=res, time_frame="", task_id=task_id, api_id="", res_id="",resq_code="")
    if request.method == "POST":
        time_frame=request.form.get('time_frame')
        task_id = request.form.get('task_id')
        api_id = request.form.get('api_id')
        res_id = request.form.get('res_id')
        resq_code = request.form.get('resq_code')
        res = task.get_rest(time_frame=time_frame,task_id=task_id,api_id=api_id,res_id=res_id,resq_code=resq_code)
        return render_template('report.html',res=res,time_frame=time_frame,task_id=task_id,api_id=api_id,res_id=res_id,resq_code=resq_code)