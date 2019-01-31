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


# @app.route('/wxtools')
# def wxtools():
# 	# lc()
# 	return render_template('wxtools.html')

@app.route('/login',methods=['post'])
def login():
	lc()
	return 'ok'


@app.route('/exit',methods=['post'])
def exit():
	ec()
	return 'ok'

@app.route('/wxtools',methods=['get','post'])
def friends_sex():
	if request.method == "POST":
		sexlist=statistic_friends_sex()
		return render_template('wxtools.html',sexlist=sexlist)
	else:
		return render_template('wxtools.html')




if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True,debug=True)