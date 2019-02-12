import os
import itchat
import threading
from pickle import *
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

def lc():
    itchat.auto_login()
    print("Finash Login!")
    pwd=os.getcwd()
    print(pwd)
    # # pwd = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    QR1=pwd.replace('\\','/')+"/static/pic/QR.png"
    os.remove(QR1)
    data=1
    return data

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


#退出登录并删除目录下二维码文件
def ec():
    itchat.logout()
    pwd=os.getcwd()
    # pwd = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    pwd=pwd.replace('\\','/')+"/static/pic/QR.png"
    if isQR()==1:
        os.remove(pwd)
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
    try:
        itchat.get_friends(update=True)
    except:
        return {"code":1001}
    else:
        return {"code":1000}
#统计好友性别
def statistic_friends_sex():
    if myfriends()=='nologin':
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
# print(statistic_friends_sex())

#统计好友城市分布
def statistic_friends_city():
    if myfriends()=='nologin':
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
            print(d)
            L.append(d)
        return L

# lc()
# print(statistic_friends_city())