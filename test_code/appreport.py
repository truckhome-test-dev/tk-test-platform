# -*- coding: utf-8 -*-
import os
import re
import time 


class APP_Report():
    """APP自动化测报告中使用到的全部函数"""


    #获取地址
    def get_url(self):
        urllist = []
        path = os.getcwd()
        path = (path + "/templates").replace('\\','/')
        apath = path + "/TestReport"

        for dir1, dir2, dir3 in os.walk(apath):

            if len(dir1) > 87:
                
                url = dir1 + '/TestReport.html'
                url = url.replace(path,"")
                url = url.replace('\\','/')
                url = url.replace(".html","")
                urllist.append(url)
        urllist = sorted(urllist,reverse=True)
        return urllist


    #获取标题与链接对应的字典
    def title_url(self):		
        titleurl = {}
        
        urllist = self.get_url()
        for i  in urllist:
            a = re.findall(r"(\d{14})",i)
            if len(a) > 0:
                title = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(a[0], '%Y%m%d%H%M%S'))
                title = title + " " + "自动化测试报告"
                titleurl.update({title:i})
        return titleurl

	
    #获取第一条报告链接
    def new_report(self):
        urls = self.get_url()
        newurl = urls[0]
        return newurl


# aa = APP_Report()
# print (aa.title_url())

