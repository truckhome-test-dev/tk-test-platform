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

# print(myfriends())

#统计好友性别
def statistic_friends_sex():
    if myfriends()=='nologin':
        return 'nologin'
    else:
        myfriend=myfriends()
        result = [0, 0, 0]
        for friend in myfriend:
            sex = friend['Sex']
            if sex == 1:
                result[0] += 1
            elif sex == 2:
                result[1] += 1
            else:
                result[2] += 1
        return str(result)[1:-1]
# print(statistic_friends_sex())

#统计好友城市分布
def statistic_friends_city():
    myfriend = myfriends()
    arr=[]
    for friend in myfriend:
        city=friend['City']
        arr.append(city)

    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result

