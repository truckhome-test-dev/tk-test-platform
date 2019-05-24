#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request, render_template, redirect, send_from_directory, abort
from test_code import *
from route import *
import json

app = Flask(__name__)
re = Device_Manag()
pt = APP_Report()
bug = Mantis_Bug()
pp = Cha_Project()
app.config.from_object('settings.DevConfig')
# token = request.cookies.get('token')

'''
这里是注册蓝图
参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
即当request.url是以/monitor的情况下才会通过注册的蓝图的视图方法处理请求并返回
'''
app.register_blueprint(monitor, url_prefix='/monitor')


@app.route('/', methods=['get'])
@app.route('/index', methods=['get'])
def index():
    return render_template('index.html')

def check_token(func):
    def inner(*args,**kwargs):
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

# 微信小工具首页
@app.route('/wxtools', methods=['get', 'post'])
def wxtools():
    if request.method == "GET":
        global login_status
        if login_status == 0:
            itinit()
        return render_template('wxtools.html')


# 查询登录状态
@app.route('/status', methods=['get', 'post'])
def status():
    data = lc_status()
    return json.dumps(data)


# 登录
@app.route('/login', methods=['post'])
def login():
    ret = lc()
    if ret == 1:
        data = {"code": 1000}
        return json.dumps(data)
    else:
        data = {"code": 1001}
        return json.dumps(data)


# 退出登录
@app.route('/exit', methods=['post'])
def exit():
    ec()
    return 'ok'


# 统计接口
@app.route('/statistic', methods=['post'])
def statistic():
    sex = statistic_friends_sex()
    Province = statistic_friends_city()
    nickname = get_nickname()
    wc1 = wc()
    if sex == "nologin" or Province == "nologin" or nickname == "nologin" or wc1 == "nologin":
        global login_status
        login_status = 0
        data = {"code": 1001}
        return json.dumps(data)
    else:
        data = {"code": 1000, "sex": sex, "Province": Province}
        return json.dumps(data)


# 排期展示
@app.route('/scheduling', methods=['get', 'post'])
def scheduling():
    name = request.args.get('name')
    if name is None:
        return render_template('scheduling.html')
    else:
        pq = Scheduling()
        data = pq.date_rest()
        return render_template('scheduling_son.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


# 设备管理展示与新增
@app.route('/device', methods=['get', 'post'])
def device():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        devtype = data['devtype']
        devsystem = data['devsystem']
        devname = data['devname']
        name = data['name']
        version = data['version']
        devnotes = data['notes']
        re.appinsp(devname, name, devnotes, version, devtype, devsystem)
        return "ok"
    else:
        alldata = re.appga()
        return render_template('device.html', alldata=alldata)


# 设备编辑后保存
@app.route('/savedev', methods=['post', 'get'])
def savedev():
    if request.method == "POST":
        devid = request.form.get('devid')
        devname = request.form.get('devname')
        devst = request.form.get('devst')
        name = request.form.get('name')
        notes = request.form.get('notes')
        version = request.form.get('version')
        re.appeditp(devname, devst, name, notes, version, devid)
        return redirect("http://127.0.0.1:5000/device")


# 修改使用状态
@app.route('/usestatus', methods=['post', 'get'])
def usestatus():
    if request.method == 'POST':
        token = request.cookies.get('token')
        data = token_check1(token)
        if data['code'] == 1000:
            devuser = request.get_data()
            devuser = json.loads(devuser.decode("utf-8"))
            devid = devuser['devid']
            user = devuser['user']
            re.appusep(devid, user)
            return "ok"
        else:
            return "no"


@app.route('/time_test', methods=['post', 'get'])
def time_test():
    if request.args.get('url'):
        url = request.args.get('url')
    else:
        url = 'http://127.0.0.1:5000/time_test_hello'
    return render_template('time_test.html', url=url)


# 响应时间测试
@app.route('/time_test_rt', methods=['post', 'get'])
def time_test_rt():
    retest = Time_Test()
    res = retest.response_time(json.loads(request.get_data().decode("utf-8"))['url'])
    return json.dumps(res)


# 响应时间测试加载页
@app.route('/time_test_hello', methods=['post', 'get'])
def time_test_hello():
    return render_template('hello.html')


# mantis_bug统计
@app.route('/bug_statistics', methods=['get', 'post'])
def bug_statistics():
    if request.method == "GET":
        L = []
        data = bug.active_version()
        sumbug = bug.bug_week()
        L.append(data)
        L.append(sumbug)
        return render_template('bug_statistics.html', data=L)


@app.route('/statistical_details', methods=['post'])
def statistical_details():
    if request.method == "POST":
        prover7 = bug.bug_prover_statistics(7)
        prover30 = bug.bug_prover_statistics(30)
        trend = bug.bug_trend()
        handler = bug.bug_handler_statistics()
        reporter = bug.bug_reporter_statistics()
        status = bug.bug_status_statistics()
        resolution = bug.bug_resolution()
        severity = bug.bug_severity()
        category = bug.bug_category()
        data = {"code": 1000, "prover7": prover7, "prover30": prover30, "trend": trend, "handler": handler,
                "reporter": reporter, "status": status, "resolution": resolution, "severity": severity,
                "category": category}
        return json.dumps(data)


# 查询手机类型
@app.route('/typedev', methods=['post', 'get'])
@check_token
def devtype():
    if request.method == 'POST':
        devtype = request.get_data()
        devtype = json.loads(devtype.decode("utf-8"))
        devtype = devtype['devtype']
        alldata = re.appga(devtype)
        return render_template('devtype.html', alldata=alldata)


# 验证token
@app.route('/token_check', methods=['post', 'get'])
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


# @app.route('/test2',methods=['post','get'])
# def test1():
# 	return render_template('test.html')


@app.route('/test1', methods=['post', 'get'])
def test2():
    data = {"code": 1000, "sex": 1, "Province": 1}
    return json.dumps(data)


# admin页面
@app.route('/admin', methods=['get', 'post'])
def admin():
    return render_template('admin.html')


# app自动化测试报告
@app.route('/appreport', methods=['post', 'get'])
def appreport():
    newreport = pt.new_report()
    reportlist = pt.title_url()
    return render_template('appreport.html', newreport=newreport, reportlist=reportlist)


# 更多报告列表
@app.route('/TestReport/<rpttime>/<dev>/TestReport', methods=['post', 'get'])
def morerpt(rpttime, dev):
    url = "TestReport/%s/%s/TestReport.html" % (rpttime, dev)
    return render_template(url)


@app.route('/test', methods=['post', 'get'])
def test():
    # data = {"code":1000,"sex": '1', "Province": '44231'}
    return render_template('index_test.html')


# flask动态路由测试
@app.route('/1/<url>', methods=['post', 'get'])
def test_1(url):
    data = "1/%s.html" % url
    return render_template(data)


# 卡车之家业务信息表
@app.route('/project_information', methods=['post', 'get'])
def Project_information():
    pp_rturn = request.args.get('firstname')
    data = pp.cha(pp_rturn)
    return render_template('project_information.html', u=data)


# 抓虫节排行榜
@app.route('/grab_bug', methods=['post', 'get'])
def grab_bug():
    grab = Grab_Bug()
    data = grab.get_bug_score()
    return render_template('grab_bug.html', data=data)


# yapi页
@app.route('/yapi', methods=['get'])
def yapi():
    return render_template('yapi.html')


@app.route('/download', methods=['get'])
def download():
    import os
    if request.method == "GET":
        # if os.path.isfile("C:/Users/zhoujian/Desktop/3.0_0.crx"):
        # return send_from_directory("C:/Users/zhoujian/Desktop","3.0_0.crx",as_attachment=True)
        if os.path.isfile("/home/YApi/3.0_0.crx"):
            return send_from_directory("/home/YApi/", "3.0_0.crx", as_attachment=True)
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
