#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request,render_template,redirect,jsonify
from test_code import *
import settings

app = Flask(__name__)
# a = Test_Tools_Api()

app.config.from_object('settings.DevConfig')


@app.route('/',methods=['get'])
@app.route('/index',methods=['get'])
def index():
    return render_template('index.html')


@app.route('/wxtools',methods=['get','post'])
def wxtools():
    if request.method == "GET":
        return render_template('wxtools.html')

@app.route('/status',methods=['get','post'])
def status():
    data=lc_status()
    return json.dumps(data)


@app.route('/login',methods=['post'])
def login():
    ret=lc()
    if ret==1:
        data={"code":1000}
        return json.dumps(data)
    else:
        data={"code":1001}
        return json.dumps(data)

@app.route('/exit',methods=['post'])
def exit():
    ec()
    return 'ok'


# @app.route('/wxtools',methods=['get','post'])
# def friends_sex():
# 	if request.method == "POST":
# 		sexlist=statistic_friends_sex()
# 		# return render_template('wxtools.html',sexlist=sexlist)
# 		return '111'
# 	else:
# 		return 'get'


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


@app.route('/devices',methods=['get','post'])
def devices():
    alldata = re.selData('devices',['devname','devstatus','name','notes'])
    devname = re.selData('devices',['devname'],1)
    return render_template('devices.html',alldata=alldata,devname=devname)


if __name__ == '__main__':
    # app.run(host='0.0.0.0',threaded=True,debug=True)
    app.run()