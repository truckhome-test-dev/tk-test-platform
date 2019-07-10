#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request, render_template, redirect, send_from_directory, abort,jsonify,url_for
from test_code import *
from route import *
from functools import wraps
from test_code.bug_calculate import *
from test_code.xmindupload import *
from test_code.to_xls import *
from werkzeug.utils import secure_filename
from xmindparser import xmind_to_xml
import json

app = Flask(__name__)
re = Device_Manag()
pt = APP_Report()
bug = Mantis_Bug()
pp = Cha_Project()
bug_calculate = Bug_Calculate()
up = Bug_Calculate()
app.config.from_object('settings.DevConfig')
# token = request.cookies.get('token')

'''
这里是注册蓝图
参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
即当request.url是以/monitor的情况下才会通过注册的蓝图的视图方法处理请求并返回
'''
app.register_blueprint(monitor, url_prefix='/monitor')


#判断登录装饰器方法
def check_token(func):
    @wraps(func)
    def inner(*args,**kwargs):
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        token_key = conf.get('token', 'key')
        token = request.cookies.get('token')
        if token == token_key:
            return func(*args, **kwargs)
        else:
            data = json.dumps({"code": 1001})
            return data
    return inner


@app.route('/', methods=['get'])
@app.route('/index', methods=['get'])
def index():
    return render_template('index.html')


# 微信小工具首页
@app.route('/wxtools', methods=['get', 'post'])
def wxtools():
    if request.method == "GET":
        global login_status
        if login_status == 0:
            itinit()
        return render_template('wxtools.html')


# 查询登录状态
@app.route('/status', methods=['get', 'post'])
def status():
    data = lc_status()
    return json.dumps(data)


# 登录
@app.route('/login', methods=['post'])
def login():
    ret = lc()
    if ret == 1:
        data = {"code": 1000}
        return json.dumps(data)
    else:
        data = {"code": 1001}
        return json.dumps(data)


# 退出登录
@app.route('/exit', methods=['post'])
def exit():
    ec()
    return 'ok'


# 统计接口
@app.route('/statistic', methods=['post'])
def statistic():
    sex = statistic_friends_sex()
    Province = statistic_friends_city()
    nickname = get_nickname()
    wc1 = wc()
    if sex == "nologin" or Province == "nologin" or nickname == "nologin" or wc1 == "nologin":
        global login_status
        login_status = 0
        data = {"code": 1001}
        return json.dumps(data)
    else:
        data = {"code": 1000, "sex": sex, "Province": Province}
        return json.dumps(data)


# 排期展示
@app.route('/scheduling', methods=['get', 'post'])
def scheduling():
    name = request.args.get('name')
    if name is None:
        return render_template('scheduling.html')
    else:
        pq = Scheduling()
        data = pq.date_rest()
        return render_template('scheduling_son.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


# 设备管理展示与新增
@app.route('/adddevice', methods=['get', 'post'])
@check_token
def addevice():
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        devtype = data['devtype']
        devsystem = data['devsystem']
        devname = data['devname']
        name = data['name']
        version = data['version']
        devnotes = data['notes']
        re.appinsp(devname, name, devnotes, version, devtype, devsystem)
        return "ok"

# 设备管理展示
@app.route('/device', methods=['get', 'post'])
def devices():
        alldata = re.appga()
        return render_template('device.html', alldata=alldata)


# 设备编辑后保存
@app.route('/savedev', methods=['post', 'get'])
def savedev():
    if request.method == "POST":
        devid = request.form.get('devid')
        devname = request.form.get('devname')
        devst = request.form.get('devst')
        name = request.form.get('name')
        notes = request.form.get('notes')
        version = request.form.get('version')
        re.appeditp(devname, devst, name, notes, version, devid)
        return redirect("http://127.0.0.1:5000/device")


# 修改使用状态
@app.route('/usestatus', methods=['post', 'get'])
@check_token
def usestatus():
    if request.method == 'POST':
        devuser = request.get_data()
        devuser = json.loads(devuser.decode("utf-8"))
        devid = devuser['devid']
        user = devuser['user']
        re.appusep(devid, user)
        return "ok"



@app.route('/time_test', methods=['post', 'get'])
def time_test():
    if request.args.get('url'):
        url = request.args.get('url')
    else:
        url = 'http://127.0.0.1:5000/time_test_hello'
    return render_template('time_test.html', url=url)


# 响应时间测试
@app.route('/time_test_rt', methods=['post', 'get'])
def time_test_rt():
    retest = Time_Test()
    res = retest.response_time(json.loads(request.get_data().decode("utf-8"))['url'])
    return json.dumps(res)


# 响应时间测试加载页
@app.route('/time_test_hello', methods=['post', 'get'])
def time_test_hello():
    return render_template('hello.html')


# mantis_bug统计
@app.route('/bug_statistics', methods=['get', 'post'])
def bug_statistics():
    if request.method == "GET":
        L = []
        data = bug.active_version()
        sumbug = bug.bug_week()
        L.append(data)
        L.append(sumbug)
        return render_template('bug_statistics.html', data=L)


@app.route('/statistical_details', methods=['post'])
def statistical_details():
    if request.method == "POST":
        prover7 = bug.bug_prover_statistics(7)
        prover30 = bug.bug_prover_statistics(30)
        trend = bug.bug_trend()
        handler = bug.bug_handler_statistics()
        reporter = bug.bug_reporter_statistics()
        status = bug.bug_status_statistics()
        resolution = bug.bug_resolution()
        severity = bug.bug_severity()
        category = bug.bug_category()
        data = {"code": 1000, "prover7": prover7, "prover30": prover30, "trend": trend, "handler": handler,
                "reporter": reporter, "status": status, "resolution": resolution, "severity": severity,
                "category": category}
        return json.dumps(data)


# 查询手机类型
@app.route('/typedev', methods=['post', 'get'])
def devtype():
    if request.method == 'POST':
        devtype = request.get_data()
        devtype = json.loads(devtype.decode("utf-8"))
        devtype = devtype['devtype']
        alldata = re.appga(devtype)
        return render_template('devtype.html', alldata=alldata)


# 验证token
@app.route('/token_check', methods=['post', 'get'])
def token_check():
    if request.method == 'POST':
        global token
        token = request.get_data()

        if token == b'':
            token = request.cookies.get('token')
        else:
            token = json.loads(token.decode("utf-8"))
            token = str(token['token'])
        data = token_check1(token)
        return json.dumps(data)
    else:
        return render_template('admin.html')


# @app.route('/test2',methods=['post','get'])
# def test1():
# 	return render_template('test.html')


@app.route('/test1', methods=['post', 'get'])
def test2():
    data = {"code": 1000, "sex": 1, "Province": 1}
    return json.dumps(data)


# admin页面
@app.route('/admin', methods=['get', 'post'])
def admin():
    return render_template('admin.html')


# app自动化测试报告
@app.route('/appreport', methods=['post', 'get'])
def appreport():
    newreport = pt.new_report()
    reportlist = pt.title_url()
    return render_template('appreport.html', newreport=newreport, reportlist=reportlist)


# 更多报告列表
@app.route('/TestReport/<rpttime>/<dev>/TestReport', methods=['post', 'get'])
def morerpt(rpttime, dev):
    url = "TestReport/%s/%s/TestReport.html" % (rpttime, dev)
    return render_template(url)


@app.route('/test', methods=['post', 'get'])
def test():
    # data = {"code":1000,"sex": '1', "Province": '44231'}
    return render_template('index_test.html')


# flask动态路由测试
@app.route('/1/<url>', methods=['post', 'get'])
def test_1(url):
    data = "1/%s.html" % url
    return render_template(data)


# 卡车之家业务信息表
@app.route('/project_information', methods=['post', 'get'])
def Project_information():
    pp_rturn = request.args.get('firstname')
    data = pp.cha(pp_rturn)
    return render_template('project_information.html', u=data)


# 抓虫节排行榜
@app.route('/grab_bug', methods=['post', 'get'])
def grab_bug():
    grab = Grab_Bug()
    data = grab.get_bug_score()
    return render_template('grab_bug.html', data=data)


# yapi页
@app.route('/yapi', methods=['get'])
def yapi():
    return render_template('yapi.html')


@app.route('/download', methods=['get'])
def download():
    import os
    if request.method == "GET":
        # if os.path.isfile("C:/Users/zhoujian/Desktop/3.0_0.crx"):
        # return send_from_directory("C:/Users/zhoujian/Desktop","3.0_0.crx",as_attachment=True)
        if os.path.isfile("/home/YApi/3.0_0.crx"):
            return send_from_directory("/home/YApi/", "3.0_0.crx", as_attachment=True)
        abort(404)

#bug计算率页联动
@app.route('/selecttwo',methods=['post','get'])
def bug_selecttwo():
    
    if request.method == 'POST':
        project = request.form.get('project')
        pr = bug.get_pro_chi(project)
        return jsonify(pr)
    else:
        return null
#bug计算率页联动
@app.route('/selectthree',methods=['post','get'])
def bug_selectthree():
    
    if request.method == 'POST':
        proname = request.form.get('proname')
        vr = bug.get_version(proname)
        return jsonify(vr)
    else:
        return null

#bug计算率
@app.route('/bug_calculate',methods=['post','get'])
def bug_calculate1():
    v = bug_calculate.countbug()
    vn = bug.get_pro()
    if request.method == 'POST':
        addtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        vname = request.form.get('project')
        proname = request.form.get('proname')
        versionname = request.form.get('versionname')
        name = request.form.get('name')
        checknum = request.form.get('checknum')
        fristnum = request.form.get('fristnum')
        leaknum = request.form.get('leaknum')
        newnum = request.form.get('newnum')
        bugcount = request.form.get('bugcount')
        #bug密度
        if float(checknum) == 0:
            bugdensity = 0
        else:
            bugdensity = '%.2f'%(float(bugcount)/float(checknum))
        #首轮漏测率
        if float(bugcount) == 0:
            fristleak = 0
        else:
            fristleak = '%.2f'%(float(leaknum)/float(bugcount))
        #引入错误率
        if float(fristnum) == 0 and float(leaknum) == 0:
            bringerror = 0
        else:
            bringerror = '%.2f'%(float(newnum)/(float(fristnum)+float(leaknum)))
        bug_calculate.bugInsert(vname,proname,versionname,name,checknum,fristnum,leaknum,newnum,bugcount,bugdensity,fristleak,bringerror,addtime)
        # data=bug_calculate.getInfor(name)
        data=bug_calculate.getInfor()

        return render_template('bug_calculate.html',data=data,v=v)

    else:
        return render_template('bug_calculate.html',data=("","",""),vn=vn,v=v)

# bug率统计检查点
@app.route('/calculate',methods=['post','get'])
def bug_calculate2():
    if request.method == 'POST':
        da = bug_calculate.getInfor1()
        json_list = []
        for i in da:
            d = {}
            d["proname"] = i[2]
            d["versionname"] = i[3]
            d["checknum"] = i[5]
            json_list.append(d)
        data = json.dumps(json_list)
        return data   
    else:
        return render_template('calculate.html',data=("","",""))

#bug率统计
@app.route('/calcu',methods=['post','get'])
def calcu():
    if request.method == 'POST':
        du = bug_calculate.bugselect()
        json_list = []
        for j in du:
            a = {}
            a["addtime"] = j[1]
            a["density"] = j[2]
            a["leakage"] = j[3]
            a["lead"] = j[4]
            json_list.append(a)
        dataa = json.dumps(json_list)
        return dataa  
    else:
        return render_template('calculate.html',data=("","",""))


#xmind上传下载
@app.route('/upload',methods=['post','get'])
def upload():
    a = up.filelist()
    if request.method == 'POST':
        f = request.files['file']
        up.fileupload(f)    
        #将xmind转为excel
        x_c = f.filename[0:-6]
        x_a = xmind_to_xx('tmp/', f.filename, x_c)
        x_a.to_excel(x_a.data_dict[0]['topic'])
        x_a.save_xls()
        #合并单元格
        x_b = style_excel('tmp/xls/', x_c+'.xls', x_a.data_dict[0]['topic']['title'])
        x_b.merge_excel(x_b.calculate())
        x_b.save_style_excel('tmp/xls/'+x_c+'.xls')
        # up.fileinsert(f.filename)
        a.append(f.filename)
        return "1"
    else:
        return render_template('upload.html',a = a)
 
#下载  
@app.route('/export_xls/<filename>', methods=['get'])
def return_file(filename):
    import os
    if request.method == "GET":
        file_dir = os.path.join('tmp/xls',filename)
        if os.path.isfile(file_dir):
            return send_from_directory("tmp/xls", filename, as_attachment=True)
        abort(404)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
