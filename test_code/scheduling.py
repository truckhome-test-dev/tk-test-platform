#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-29 17:08:26
import requests
import json

class Scheduling(object):
	"""docstring for Test_Tools_Api"""

	def get_default_data(self):
		url = 'http://venus.360che.com/server/admin.php/Task/ganTe'
		data = {'start_date':'2018-12-31', 'end_date':'2019-03-01', 'department_id':'0'}
		paiqi_json = requests.post(url, data=data)
		# print(paiqi_json.text)
		aa = paiqi_json.text
		return paiqi_json.json()
print('你好')
a = Scheduling()
b = a.get_default_data()
# print(type(b))
# print(a.get_default_data()[0])
# print(a.get_default_data().json())
print(b['data'])

# for i,o in b.items():
# 	print(i)
