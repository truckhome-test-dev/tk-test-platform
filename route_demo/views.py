#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2019/11/7 19:20
# @Author  : Mr. Cui
# @File    : views.py
# @Software: PyCharm
from flask import Blueprint, render_template
route_demo = Blueprint('route_demo', __name__)

@route_demo.route('/')
def index():
    return render_template('route_demo/index.html')