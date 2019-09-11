# -*- coding: utf-8 -*-
import os
import re
import time
import requests
import pysnooper

class APP_Report():
    """APP自动化测报告中使用到的全部函数"""

    def get_text(self,type1):
        # 获取报告第一级别页面内容
        if type1==1:
            url = "http://192.168.20.20/TestReport/"
        else:
            url = "http://192.168.20.20/WebReport/"
        retext = requests.get(url).text
        return retext

    def get_title(self,type1):
        # 通过访问20地址获取自动化报告日期
        titlelist = []

        retext = self.get_text(type1)
        if type1 == 1:
            dates = re.findall(r'href="Report_(.+)/">', retext)
            for i in dates:
                title = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(i, '%Y%m%d%H%M%S'))
                title = title + "  " + "APP自动化测试报告"
                titlelist.append(title)
        else:
            dates = re.findall(r'\[DIR\]"></td><td><a href="(.+)/">', retext)
            for i in dates:
                title = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(i, '%Y%m%d%H%M%S'))
                title = title + "  " + "Web自动化测试报告"
                titlelist.append(title)
        if type1 == 1:
            titlelist = sorted(titlelist, reverse=True)
        else:
            titlelist = sorted(titlelist, reverse=True)[-24:]
        return titlelist

    # @pysnooper.snoop()
    def get_url(self,type1):
        # 获取链接地址
        devlist = []
        datelist = []
        urllist = []
        retext = self.get_text(type1)
        urls = re.findall(r'a href="(.+)/">', retext)
        urls = sorted(urls, reverse=True)
        for i in urls:
            if type1 == 1:
                url = "http://192.168.20.20/TestReport/" + i
                datelist.append(url)
            else:
                url = "http://192.168.20.20/WebReport/" + i
                urllist.append(url)
        if type1 == 1:
            for j in datelist:
                retext = requests.get(j).text
                dev = (re.findall(r'\[DIR\]"></td><td><a href="(.+)/">', retext))[0]
                devlist.append(dev)
            for m, n in zip(datelist, devlist):
                url = m + '/' + n + '/TestReport.html'
                urllist.append(url)

        return urllist


    def title_url(self,type1):

        # 获取标题与链接的字典
        titlelist = self.get_title(type1)
        urllist = self.get_url(type1)
        title_url = {}

        for i, j in zip(titlelist, urllist):
            title_url.update({i: j})

        return title_url


    def new_report(self,type1):
        # 获取最新报告链接

        urls = self.get_url(type1)
        if type1 == 1:
            newurl = urls[0]
        else:
            newurl = [urls[0]+"/bbs.html",urls[0]+"/product.html",urls[0]+"/information.html"]
        return newurl


# a = APP_Report()
# d = a.get_title(2)

# print (d)

