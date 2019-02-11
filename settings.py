#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44


class BaseConfig(object):
	# 公用的配置
	host = '0.0.0.0'
	DEBUG = True
	TESTING = True
	THREADED = True

class TestConfig(BaseConfig):
	DB = '127.0.0.1'	

class DevConfig(BaseConfig):
	host = '0.0.0.0'




