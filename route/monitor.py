#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect,url_for
from test_code import *
from functools import wraps
import json
import pysnooper

# 创建蓝图对象
monitor = Blueprint('monitor', __name__)
task = Monitor_Task()
api = Api_Monitor()
res = Monitor_Res()
mm = Monitor_Mongodb()
strategy = Monitor_Inform()

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
# @check_permissions("/monitor/task_list")
def task_list():
    if request.method == "GET":
        task_list = task.task_list()
        return render_template('task.html', task_list=task_list)


# 编辑任务
@monitor.route('/task_edit', methods=['get', 'post'])
#@check_permissions("/monitor/task_edit")
def task_edit():
    if request.method == "GET":
        title = "编辑任务"
        task_id = request.args.to_dict().get('task_id', "")
        task_info = task.task_info(task_id)
        api = "task_edit"
        return render_template('task_edit.html', api=api, title=title, task_info=task_info)
    else:
        data = request.get_data()
        data = json.loads(data)
        task_id = data['task_id']
        task_name = data['task_name']
        frequency = data['frequency']
        inform = data['inform']
        api_id = data['apis']
        # api_id = "11"
        start_inform = data['start_inform']
        stop_inform = data['stop_inform']
        re_inform = data['re_inform']
        if inform == 0:
            token = data['token']
            re_email = data['email']
            task.task_edit(task_id, task_name, api_id, frequency,start_inform,stop_inform,re_inform,inform,token,re_email)
        else:
            task.task_edit(task_id, task_name, api_id, frequency,start_inform,stop_inform,re_inform,inform)
        return "ok"

#添加任务
@monitor.route('/task_add', methods=['get', 'post'])
@check_permissions("/monitor/task_add")
def task_add():
    if request.method == "GET":
        title = "添加任务"
        task_info = ("", "", "", "3", "","","","","","","1")
        api = "task_add"
        return render_template('task_edit.html', api=api, title=title, task_info=task_info)
    else:
        data = request.get_data()
        data = json.loads(data)
        task_name = data['task_name']
        frequency = data['frequency']
        api_id = data['apis']
        start_inform = data['start_inform']
        stop_inform = data['stop_inform']
        re_inform = data['re_inform']
        inform = data['inform']
        if inform == 0:
            token = data['token']
            re_email = data['email']
            task.task_add(task_name, api_id, frequency,start_inform,stop_inform,re_inform,inform,token,re_email)
        else:
            task.task_add(task_name, api_id, frequency,start_inform,stop_inform,re_inform,inform)
        return "ok"

# 删除任务
@monitor.route('/task_del', methods=['get', 'post'])
@check_permissions("/monitor/task_del")
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
@check_permissions("/monitor/task_status")
def task_status():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        task_id = data['task_id']
        ret = task.run(task_id)
        return ret


# 监控平台接口新增
@monitor.route('/newapi', methods=['post', 'get'])
@check_permissions("/monitor/newapi")
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
        return render_template('apilist.html', apidata2=apidatas, prolist=prolist, count=count, proid=0)
    else:
        proid = request.form.get('proid')
        if proid != None:
            prolist = api.prolist()
            apidatas = api.proapi(proid, page=0)
            count = len(api.proapi(proid, count=1))
            return render_template('apilist.html', apidata2=apidatas, prolist=prolist, proid=proid, count=count)
        else:
            page = request.get_data()
            page = json.loads(page.decode("utf-8"))
            page = page['page']
            proid = request.get_data()
            proid = json.loads(proid.decode("utf-8"))
            proid = proid['proid']
            apidatas = api.proapi(proid, page=page)
            prolist = api.prolist()
            count = len(api.proapi(proid, count=1))
            return render_template('apipage.html', apidata2=apidatas, prolist=prolist, count=count)


# 监控平台修改接口内容
@monitor.route('/api', methods=['post', 'get'])
@check_permissions("/monitor/api")
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
@check_permissions("/editstatus")
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


# 接口请求记录

@monitor.route('/report', methods=['get', 'post'])
# @check_permissions("/monitor/report")
def report():
    if request.method == "GET":
        task_id = request.args.to_dict().get('task_id', "")
        res = task.get_rest(task_id=task_id, page=1)
        count = task.get_count()  # 查询所有的总数
        return render_template('report.html', res=res, count=count)
    else:
        data = request.get_data()  # 获取页数的编号
        data = json.loads(data.decode("utf-8"))  # json.loads函数的使用
        # 传入参数获取到需要的条件
        time_frame = data['time_frame']  # 时间表
        task_id = data['task_id']  # 任务
        api_id = data['api_id']  # 接口
        res_id = data['res_id']  # 编号
        # print(res_id)
        resq_code = data['resq_code']  # 结果
        page = data['page']  # 从前端获取页数
        res = task.get_rest(page=page, time_frame=time_frame, task_id=task_id, api_id=api_id, res_id=res_id,
                            resq_code=resq_code)
        return render_template('reportpage.html', res=res)  # 返回数据进行处理将每页多少条进行处理后返回給模板进行填充


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
# @check_permissions("/monitor/result")
def result():
    tasklist = task.task_list()
    # group = mm.get_group()
    if request.method == 'GET':
        mydate = res.get_time()
        return render_template('result.html', tasklist=tasklist, mydate=mydate)
    else:
        task_id = request.get_data()
        task_id = json.loads(task_id.decode("utf-8"))
        task_id = task_id['task_id']
        time_frame = request.get_data()
        time_frame = json.loads(time_frame.decode("utf-8"))
        time_frame = time_frame['time_frame']

        taskstatis = res.get_task_statistics(task_id, time_frame=time_frame)
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
        rt = res.api_rt(api_id, time_frame=time_frame)
        data = {"code": 1000, "t": rt[0], "r": rt[1],"avg_r":int(sum(rt[1])/len(rt[1]))}
        return json.dumps(data)


@monitor.route('/get_apiname', methods=['get', 'post'])
def get_apiname():
    if request.method == 'POST':
        pro_name = request.get_data()
        pro_name = json.loads(pro_name.decode("utf-8"))
        pro_name = pro_name['pro_name']

        api_name = res.get_api(pro_name)
        if api_name:
            data = {"code": 1000, "api_name": api_name}
        else:
            data = {"code": 1002, "api_name": api_name}
        return json.dumps(data)


# 获取接口列表，根据不同type获取对应列表
@monitor.route('/get_interface_list', methods=['post'])
def get_interface_list():
    try:
        # 获取json数据
        # data = request.get_data()
        # data = json.loads(data.decode("utf-8"))
        # type = data['type']
        # id = data['id']
        # 获取form数据
        type = request.form.get('type')
        id = int(request.form.get('id'))
        if type == "group":
            data = mm.get_group()
        elif type == 'project':
            data = mm.get_project(id)
        elif type == 'cat':
            data = mm.get_interface_cat(id)
        elif type == 'interface':
            data = mm.get_interface(id)
        else:
            data = '参数异常'
        if data == '参数异常':
            ret = {"code": 1003, "data": data}
            # ret={"status": 0,"message": "","total": 180,"data": {"item": data }}
        else:
            ret = {"code": 1000, "data": data}
            # ret = {"code": 0, "message": "", "total": 180, "data": data}
    except:
        ret = {"code": 1003, "data": "参数异常"}
    return json.dumps(ret)


#开启通知
@monitor.route('/switch', methods=['post','get'])
def swich():
    if request.method=="GET":
        return render_template('switch.html')
    else:
        type = request.form.get('type')
        id = int(request.form.get('id'))
        val=int(request.form.get('val'))
        if type == "status":
            data=strategy.get_interface_status(id)
            ret="监控状态：%s \n通知状态：%s"%(data[0],data[1])
            ret=ret.replace("1","开启").replace("0","关闭")
            return ret
        else:
            strategy.update_interface_status(type, id, val)
            return "更新成功！"

#数据表用
@monitor.route('/new_get_interface_list', methods=['get'])
def new_get_interface_list():
    try:
        # 获取json数据
        # data = request.get_data()
        # data = json.loads(data.decode("utf-8"))
        # type = data['type']
        # id = data['id']
        # 获取form数据
        type = request.args.get('type')
        id = int(request.args.get('id'))
        if type == "group":
            data = mm.get_group()
        elif type == 'project':
            data = mm.get_project(id)
        elif type == 'cat':
            data = mm.get_interface_cat(id)
        elif type == 'interface':
            data = mm.get_interface(id)
        else:
            data = '参数异常'
        if data == '参数异常':
            # ret = {"code": 1003, "data": data}
            ret={"status": 0,"message": "","total": 180,"data": {"item": data }}
        else:
            # ret = {"code": 1000, "data": data}
            ret = {"code": 0, "message": "", "total": 180, "data": data}
    except:
        ret = {"code": 1003, "data": "参数异常"}
    return json.dumps(ret)


@monitor.route('/statis_show', methods=['get'])
def statis_show():
    task_id=request.args.get('task_id')
    time=request.args.get('time')
    s=StatisShow()
    err_data=s.statis_err(task_id,time)
    timeout_data=s.statis_timeout(task_id,time)
    return render_template('statis_show.html',err_data=err_data,timeout_data=timeout_data)