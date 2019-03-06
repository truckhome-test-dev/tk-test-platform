#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request,render_template,redirect,jsonify
from test_code import *
import settings
import json

app = Flask(__name__)
re = Device_Manag()

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


@app.route('/scheduling',methods=['get','post'])
def scheduling(name=None):
    if not name:
        pq = Scheduling()
        return pq.get_default_data()
    else:
        pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

#设备管理展示与新增
@app.route('/devices',methods=['get','post'])
def devices():
    if request.method == "POST":
        devname = request.form.get('devname')
        devtype = request.form.get('devtype')
        name = request.form.get('name')
        devnotes = request.form.get('devnotes')
        deversion = request.form.get('deversion')
        re.appinsp(devname,devtype,name,devnotes,deversion)
        return redirect("http://127.0.0.1:5000/devices")
    else:
        alldata = re.appga()
        return render_template('devices.html',alldata=alldata)
        

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
        return redirect("http://127.0.0.1:5000/devices")


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





if __name__ == '__main__':
	app.run()


