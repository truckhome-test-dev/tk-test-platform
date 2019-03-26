import os
import itchat
import threading
from pickle import *
from os import path
from PIL import Image
import numpy as np
# import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from configparser import ConfigParser

global login_status
login_status=0
pwd=os.getcwd()
#多线程，暂时未用到
class MyThread(threading.Thread):

    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def lcisQR():
    threads = []
    t1 = threading.Thread(target=isQR,args=())
    threads.append(t1)
    t2 = threading.Thread(target=lc,args=())
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

#登录
def lc():
    itchat.auto_login()
    global login_status
    login_status = 1
    print("Finash Login!")
    pwd=os.getcwd()
    # # pwd = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    QR1=pwd.replace('\\','/')+"/static/pic/QR.png"
    os.remove(QR1)
    data=1
    return data

#清除登录状态
def itinit():
    ec()
    QR = pwd.replace('\\', '/') + "/static/pic/QR.png"
    RemarkName = pwd.replace('\\', '/') + "/static/pic/RemarkName.png"
    if os.path.exists(QR):
        os.remove(QR)
    if os.path.exists(RemarkName):
        os.remove(RemarkName)

#判断目录下是否存在登录二维码
def isQR():
    status=0
    pwd=os.getcwd()
    # pwd = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    pwd=pwd.replace('\\','/')+"/static/pic/QR.png"
    if os.path.exists(pwd):
        status=1
        return status
    else:
        return status

#退出登录并删除目录下二维码文件
def ec():
    itchat.logout()
    global login_status
    login_status = 0
    RemarkName=pwd.replace('\\','/')+"/static/pic/RemarkName.png"
    if os.path.exists(RemarkName):
        os.remove(RemarkName)
    print("exit")

#获取微信好友信息
def myfriends():
    try:
        data = itchat.get_friends(update=True)
    except:
        return 'nologin'
    else:
        return data

#判断登录状态
def lc_status():
    global login_status
    if login_status == 0:
        data = {"code": 1001}
        return data
    else:
        data = {"code": 1000}
        return data

#统计好友性别
def statistic_friends_sex():
    if login_status == 0:
        return 'nologin'
    else:
        myfriend=myfriends()
        result = [0, 0, 0]
        sexname=['男','女','其他']
        for friend in myfriend:
            sex = friend['Sex']
            if sex == 1:
                result[0] += 1
            elif sex == 2:
                result[1] += 1
            else:
                result[2] += 1
        L = []
        for i in sexname:
            d = {}
            d['name'] = i
            L.append(d)
        for i in range(3):
            L[i]['value'] = result[i]
        return L

#统计好友城市分布
def statistic_friends_city():
    if login_status == 0:
        return 'nologin'
    else:
        myfriend = myfriends()
        arr=[]
        for friend in myfriend:
            # City=friend['City']
            Province=friend['Province']
            arr.append(Province)
        result = {}
        for i in set(arr):
            result[i] = arr.count(i)
        L=[]
        for i in result.items():
            d = {}
            d["name"]=i[0]
            d["value"]=i[1]
            # print(d)
            L.append(d)
        return L

#获取微信好友昵称
def get_nickname():
    if login_status == 0:
        return 'nologin'
    else:
        text=""
        myfriend=myfriends()
        for friend in myfriend:
            RemarkName=friend['RemarkName']
            if RemarkName=='':
                RemarkName=friend['NickName']
            text += (RemarkName+" ")
        RemarkName = pwd.replace('\\', '/') + "/static/conf/RemarkName.txt"
        # print(text)
        f=open(RemarkName,"wt",encoding='utf-8')
        f.write(text)
        f.close()
    print('ok')

#词云
def wc():
    if login_status == 0:
        return 'nologin'
    else:
        # current path
        d = path.dirname(__file__)
        # print(d)
        # print(os.getcwd())
        RemarkName = pwd.replace('\\', '/') + "/static/conf/RemarkName.txt"

        # 用于生成词云的文本
        text = open(RemarkName,encoding='utf-8').read()

        # 图片模板
        test_mask = np.array(Image.open(pwd.replace('\\', '/') + "/static/pic/test_mask.png"))
        simfang = pwd.replace('\\', '/') + "/static/conf/simfang.ttf"
        stopwords = set(STOPWORDS)
        stopwords.add("said")

        # setting
        wc = WordCloud(font_path=simfang, background_color="white", max_words=2000, mask=test_mask,
                       stopwords=None, scale=2)
        # 生成词云
        try:
            wc.generate_from_text(text)
        except:
            return 'nologin'

        # 制图  mac不支持
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off")
        # plt.figure()
        # plt.imshow(test_mask, cmap=plt.cm.gray, interpolation='bilinear')
        # plt.axis("off")
        # plt.show()

        # 保存文件
        RemarkNamePic = pwd.replace('\\', '/') + "/static/pic/RemarkName.png"
        wc.to_file(path.join(d, RemarkNamePic))
