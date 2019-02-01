#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request,render_template,redirect,jsonify
import json
from test_code import *

app = Flask(__name__)
# a = Test_Tools_Api()




@app.route('/',methods=['get'])
@app.route('/index',methods=['get'])
def index():
	return render_template('index.html')


@app.route('/wxtools')
def wxtools():
	# lc()
	return render_template('wxtools.html')

@app.route('/login',methods=['post'])
def login():
	lc()
	if lc()==1:
		data={"code":1000}
		return json.dumps(data)
	else:
		data={"code":1001}
		return json.dumps(data)

@app.route('/exit',methods=['post'])
def exit():
	ec()
	return 'ok'

@app.route('/statistic',methods=['post'])
def statistic():
	sex = statistic_friends_sex()
	Province = statistic_friends_city()
	if sex =="nologin" or Province =="nologin":
		data={"code":1001}
		return json.dumps(data)
	else:
		data = {"code":1000,"sex": sex, "Province": Province}
		return json.dumps(data)




if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True,debug=True)