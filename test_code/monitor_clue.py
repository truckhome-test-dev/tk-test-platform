#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2019/9/12 11:42
# @Author  : Mr. Cui
# @File    : test.py
# @Software: PyCharm
import requests
import time
import json
import datetime


def DasMgt():
    url = "http://saasms.360che.com.cn/DasMgt/Home/Ajax_GetCluesList"
    today = datetime.date.today()
    params = {
        "TonnageId": -1,
        "Category": 0,
        "SubCategory": 0,
        "Brand": 0,
        "Series": 0,
        "Province": 0,
        "City": "请选择市",
        "FollowupTotal": "",
        "PublicPool": "",
        "PublicPoolGetCount": -1,
        "CluesSource": "",
        "CluesState": "",
        "orderby": "Createdate desc",
        "start_time": today,
        "end_time": today,
        "keyType": "tel",
        "key": "",
        "pagesize": 20,
        "currentPage": 1,
    }
    headers = {
        "Cookie": '_ga=GA1.3.565701365.1566268471; THCookieName=G1oc5kGzJu02KtNaqLk1ytBQCit2K6nMgl/IvoDC+HLb1xvPIfshjYM6N6/EAUDJAnvXnSjWoCKlnS+FdFpA7c5bxAQbuFuwcuUxnn+RzDpioL1/LK8t0io2sME5ASABfk8Y4YdWMfA=; thcookienmnew=dvSzqXIfAZR0B++/HrCST8fWg2M/4XlrwIPSTQbqruhdrtSv5wrNRVIefs/4YTrD0i3AQNUGQAbUC2kdW33odZ3haP0YEdzxjwLBmcn3yrLf+y2vCw8fOVhFCq9xth5rHw6lni+YgPw=; COOKIENAME_DealerSaasManagement_Account_Dealer_DH={"Id":711,"AccountId":99255,"RealName":"å´éæ","Department":63,"ILevel":0,"Provinceleng":"","Cityleng":""}; SERVER_ID=adf81139-ca6b6263'}
    ret = requests.post(url, headers=headers,params=params)
    return ret.json()


def sending(token, content):
    HEADERS = {"Content-Type": "application/json ;charset=utf-8 "}
    data = {"msgtype": "text", "text": {"content": content}, "at": {"atMobiles": [], "isAtAll": "false"}}
    data = json.dumps(data)
    res = requests.post(token, data=data, headers=HEADERS)


def func():
    token = "https://oapi.dingtalk.com/robot/send?access_token=7eb86685e144cb9a048f2a266c46b36dd458bec91ca9f2c1bbecf6b53a6e05ab"
    data = DasMgt()['html']
    print(data)
    if len(data) > 0:
        sp = int(time.time())
        for i in data:
            ClueResource = i['ClueResource']
            Createdate = str(i['Createdate']).replace('<br/> ', "")
            Createdate = int(time.mktime(time.strptime(Createdate, "%Y-%m-%d %H:%M:%S")))
            print(ClueResource, Createdate)
            break
        if sp - Createdate < 180:
            print("ok")
        else:
            content = "3分钟之内无新线索，请注意"
            sending(token, content)
    else:
        content = "当天无线索"
        sending(token, content)


if __name__ == '__main__':
    func()