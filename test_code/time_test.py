#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-29 17:08:26
import requests


class Time_Test(object):
	"""接口查询管理"""
	
	def response_time(self, url):
		url = self.dis_url(url)
		try:
			respones = self.response_info(requests.get(url))
		except requests.exceptions.ConnectionError as e:
			respones = {'info':'请求出错','报错信息':str(e)}
		# respones = requests.get(url)
		except requests.exceptions.InvalidURL as e:
			respones = {'info':'无效url','报错信息':str(e)}
		return respones


	def dis_url(self, url):
		if 'http://' in url or 'https://' in url:
			okurl = url
		else:
			okurl = 'http://' + url 
		return okurl


	def response_info(self, respones):
		#info = {'Content-Type':'内容类型', 'Server':'服务', }
		re_info = {'respones_time':'%.2fms' % (respones.elapsed.microseconds/1000), 'Status':respones.status_code}
		for v,i in respones.headers.items():
			re_info[v]=i
		return re_info


