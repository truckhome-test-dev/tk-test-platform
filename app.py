#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request,render_template,redirect,jsonify
import json
from test_code import *

app = Flask(__name__)
re = Device_Manag()




@app.route('/',methods=['get'])
@app.route('/index',methods=['get'])
def index():
	return render_template('index.html')


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


@app.route('/devices',methods=['get','post'])
def devices():
	if request.method == "POST":
		devname = request.form.get('devname')
		devtype = request.form.get('devtype')
		name = request.form.get('name')
		devnotes = request.form.get('devnotes')
		re.appinsp(devname,devtype,name,devnotes)
		return redirect("http://127.0.0.1:5000/devices")
	else:
		alldata = re.appga()
		devname = re.appgd()
		return render_template('devices.html',alldata=alldata,devname=devname)
        

@app.route('/selectdev',methods=['post','get'])
def seldev():
	if request.method == "POST":
		seadev = request.get_data()
		seldata = re.appseap(seadev)
		return seldata


@app.route('/deldev',methods=['post','get'])
def deldev():
	if request.method == "POST":
		devdata = request.get_data()		
		re.appdelp(devdata)
		return 'ok'


@app.route('/editdev',methods=['post','get'])
def editdev():
	if request.method == "GET":
		devid = request.args.to_dict().get('devid', "")
		data = re.appeditg(devid)	
		return render_template('editdev.html',editdata=data)


@app.route('/savedev',methods=['post','get'])
def savedev():
	if request.method == "POST":
		devid = request.form.get('devid')
		devname = request.form.get('devname')
		devst = request.form.get('devst')
		name = request.form.get('name')
		notes = request.form.get('notes')
		re.appeditp(devname,devst,name,notes,devid)
		return redirect("http://127.0.0.1:5000/devices")   

if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True,debug=True)