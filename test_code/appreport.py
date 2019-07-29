# -*- coding: utf-8 -*-
import os
import re
import time
import requests


class APP_Report():
    """APP自动化测报告中使用到的全部函数"""

    def get_text(self):
        # 获取第一级别页面内容
        url = "http://192.168.20.20/TestReport/"
        retext = requests.get(url).text
        return retext

    def get_title(self):
        # 通过访问20地址获取日期
        titlelist = []
        retext = self.get_text()
        dates = re.findall(r'href="Report_(.+)/">', retext)
        for i in dates:
            title = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(i, '%Y%m%d%H%M%S'))
            title = title + "  " + "自动化测试报告"
            titlelist.append(title)

        titlelist = sorted(titlelist, reverse=True)
        return titlelist

    def get_url(self):
        # 获取链接地址
        devlist = []
        datelist = []
        urllist = []
        retext = self.get_text()
        urls = re.findall(r'a href="(.+)/">', retext)
        urls = sorted(urls, reverse=True)
        for i in urls:
            url = "http://192.168.20.20/TestReport/" + i
            datelist.append(url)
        for j in datelist:
            retext = requests.get(j).text
            dev = (re.findall(r'\[DIR\]"></td><td><a href="(.+)/">', retext))[0]
            devlist.append(dev)
        for m, n in zip(datelist, devlist):
            url = m + '/' + n + '/TestReport.html'
            urllist.append(url)

        return urllist

    def title_url(self):
        # 获取标题与链接的字典
        titlelist = self.get_title()
        urllist = self.get_url()
        title_url = {}

        for i, j in zip(titlelist, urllist):
            title_url.update({i: j})

        return title_url

    def new_report(self):
        # 获取最新报告链接
        urls = self.get_url()
        newurl = urls[0]
        return newurl
