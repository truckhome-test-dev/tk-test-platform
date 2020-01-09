# -*- coding: utf-8 -*-
import os
import re
import time
import requests
import pysnooper


def timeit(f):
    def wrapper(*args, **kwargs):       
        start_time = time.time()      
        res = f(*args, **kwargs)
        end_time = time.time()          
        print("%s函数运行时间为：%.8f" %(f.__name__, end_time - start_time))
        return res        
    return wrapper  

class APP_Report():
    """APP自动化测报告中使用到的全部函数"""
    def __init__(self,type1):
        self.gettext = self.get_text(type1)


    # @timeit
    def get_text(self,type1):
        # 获取报告第一级别页面内容
        if type1==1:
            url = "http://192.168.20.20/TestReport/"
        else:
            url = "http://192.168.20.20/WebReport/"
        retext = requests.get(url).text
        urls = re.findall(r'a href="(.+)/">', retext)
        urls = sorted(urls, reverse=True)
        return urls


    # @timeit
    def get_title(self,type1,parms):
        if type1 == 1:
            title = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(parms, '%Y%m%d%H%M%S'))
            title = title + "  " + "APP自动化测试报告"
        else:
            title = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(parms, '%Y%m%d%H%M%S'))
            title = title + "  " + "Web自动化测试报告"
        return title

    # @timeit
    def get_url(self,type1):
        # 获取链接地址
        devlist = []
        urllist1 = []
        urllist = []
        titlelist = []
        texts = self.gettext
        for i in texts:     
            if type1 == 1:
                url = "http://192.168.20.20/TestReport/" + i
                urllist1.append(url)
                times = i[-14:]
                title = self.get_title(type1,times) 
                titlelist.append(title)                  
            else:
                num = texts.index(i)
                if num < 24 :
                    times = i[-14:]
                    url = "http://192.168.20.20/WebReport/" + times                    
                    urllist.append(url)
                    title = self.get_title(type1,times)
                    titlelist.append(title)                    

        if type1 == 1:
            for j in urllist1:
                retext = requests.get(j).text
                dev = (re.findall(r'\[DIR\]"></td><td><a href="(.+)/">', retext))[0]
                devlist.append(dev)
            for m, n in zip(urllist1, devlist):
                url = m + '/' + n + '/TestReport.html'
                urllist.append(url)

        return titlelist,urllist  


    # @timeit
    def title_url(self,type1,datatype):
        # 获取标题与链接的字典
        data = self.get_url(type1)    
        titlelist = data[0]
        urllist = data[1]

        title_url = {}
        for i, j in zip(titlelist, urllist):
            title_url.update({i: j})

        newurl = urllist[0]
            
        if datatype == 1:            
            return title_url,newurl
        else:
            webnewurl = [newurl+"/bbs.html",newurl+"/product.html",newurl+"/information.html"]
            return title_url,webnewurl




# a = APP_Report(1)
# urls = a.get_url(1)
# print (urls)

# a = APP_Report(2)
# urls2 = a.title_url(2,2)
# print(urls2) 
