#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request,render_template,redirect,jsonify
from test_code import *
from test_code.mantis_bug import *
from test_code.appreport import *
import settings
import json

app = Flask(__name__)
re = Device_Manag()
pt = APP_Report()
# bug = Mantis_Bug(host='117.50.17.66',user='qa',passwd = 'k04d8gAvDJ8PkvrL',database="bugtracker")
bug=Mantis_Bug()
app.config.from_object('settings.DevConfig')


@app.route('/',methods=['get'])
@app.route('/index',methods=['get'])
def index():
    return render_template('index.html')

#微信小工具首页
@app.route('/wxtools',methods=['get','post'])
def wxtools():
    if request.method == "GET":
        return render_template('wxtools.html')
        
#查询登录状态
@app.route('/status',methods=['get','post'])
def status():
    data=lc_status()
    return json.dumps(data)

#登录
@app.route('/login',methods=['post'])
def login():
    ret=lc()
    if ret==1:
        data={"code":1000}
        return json.dumps(data)
    else:
        data={"code":1001}
        return json.dumps(data)

#退出登录
@app.route('/exit',methods=['post'])
def exit():
    ec()
    return 'ok'

#统计接口
@app.route('/statistic',methods=['post'])
def statistic():
    sex = statistic_friends_sex()
    Province = statistic_friends_city()
    nickname=get_nickname()
    wc1=wc()
    if sex =="nologin" or Province =="nologin" or nickname =="nologin" or wc1 =="nologin" :
        data={"code":1001}
        return json.dumps(data)
    else:
        data = {"code":1000,"sex": sex, "Province": Province}
        return json.dumps(data)


#排期展示
@app.route('/scheduling',methods=['get','post'])
def scheduling():
    name = request.args.get('name')
    if name is None:
        return render_template('Scheduling.html')
    else:
        pq = Scheduling()
        data = pq.date_rest()
        return render_template('Scheduling_son.html',data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

#设备管理展示与新增
@app.route('/device',methods=['get','post'])
def device():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        devtype = data['devtype']
        devname = data['devname']
        name = data['name']
        version = data['version']
        devnotes = data['notes']
        re.appinsp(devname,devtype,name,devnotes,version)
        return "ok"
    else:
        alldata = re.appga()
        return render_template('device.html',alldata=alldata)


#设备编辑后保存
@app.route('/savedev',methods=['post','get'])
def savedev():
    if request.method == "POST":
        devid = request.form.get('devid')
        devname = request.form.get('devname')
        devst = request.form.get('devst')
        name = request.form.get('name')
        notes = request.form.get('notes')
        version = request.form.get('version')
        re.appeditp(devname,devst,name,notes,version,devid)
        return redirect("http://127.0.0.1:5000/device")


#修改使用状态
@app.route('/usestatus',methods=['post','get'])
def usestatus():
    if request.method == 'POST':
        devuser = request.get_data()
        devuser = json.loads(devuser.decode("utf-8"))
        devid = devuser['devid']
        user = devuser['user']
        re.appusep(devid,user)
        return "ok"


@app.route('/time_test',methods=['post','get'])
def test(): 
    if request.args.get('url'):
        url = request.args.get('url')
    else:
        url = 'http://127.0.0.1:5000/test_1'
    return render_template('time_test.html', url=url)       


#mantis_bug统计
@app.route('/bug_statistics',methods=['get','post'])
def bug_statistics():
    if request.method == "GET":
        data=bug.activeVersion()
        return render_template('bug_statistics.html',activeVersion=data)


@app.route('/statistical_details',methods=['post'])
def statistical_details():
    if request.method == "POST":
        prover=bug.bug_prover_statistics()
        trend = bug.bug_trend()
        handler=bug.bug_handler_statistics()
        reporter=bug.bug_reporter_statistics()
        status=bug.bug_status_statistics()
        resolution=bug.bug_resolution()
        severity=bug.bug_severity()
        category=bug.bug_category()
        data = {"code":1000,"prover":prover,"trend":trend,"handler":handler,"reporter":reporter,"status":status,"resolution":resolution,"severity":severity,"category":category}
        return json.dumps(data)


@app.route('/test_1',methods=['post','get'])
def test_1():
    return render_template('hello.html') 


# 查询手机类型
@app.route('/typedev',methods=['post','get'])
def devtype():
    if request.method == 'POST':
        devtype = request.get_data()
        devtype = json.loads(devtype.decode("utf-8"))
        devtype = devtype['devtype']
        alldata = re.appga(devtype)
        return render_template('devtype.html',alldata=alldata)


@app.route('/test2',methods=['post','get'])
def test1():
	return render_template('test.html')



@app.route('/test1',methods=['post','get'])
def test2():
    data = {"code":1000,"sex": sex, "Province": Province}
    return json.dumps(data)


#app自动化测试报告
@app.route('/appreport',methods=['post','get'])
def appreport():
    newreport = pt.new_report()
    reportlist = pt.title_url()
    return render_template('appreport.html',newreport=newreport,reportlist=reportlist) 

#更多报告列表
@app.route('/TestReport/<rpttime>/<dev>/TestReport',methods=['post','get'])
def morerpt(rpttime,dev):
    url = "TestReport/%s/%s/TestReport.html" % (rpttime,dev)
    return render_template(url) 


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')


