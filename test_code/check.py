#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-28 17:08:26
import json
import configparser


def token_check1(token):
    conf = configparser.ConfigParser()
    conf.read("conf/config.ini")
    token_key = conf.get('token', 'key')
    # token_key="123"
    if token == token_key:
        data = {"code": 1000}
    else:
        data = {"code": 1001}
    return data

# print(token_check('123qwe'))
def check_token1(token):
    def wrapper(func):  # 指定宇宙无敌参数
        def inner_wrapper(*args, **kwargs):
            conf = configparser.ConfigParser()
            conf.read("conf/config.ini")
            token_key = conf.get('token', 'key')
            if token == token_key:
                return func(*args, **kwargs)
            else:
                data = json.dumps({"code": 1001})
                return data
        return inner_wrapper
    return wrapper  # 返回


