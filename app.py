#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request,render_template,redirect,jsonify
import json
from test_code import *

app = Flask(__name__)
a = Test_Tools_Api()




@app.route('/',methods=['get'])
@app.route('/index',methods=['get'])
def index():
	return render_template('index.html')

@app.route('/index',methods=['get'])
def home():
	return render_template('home.html')

@app.route('/test')
def test():
	return a.list1()


if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True,debug=True)