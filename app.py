#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 16:19:44

from flask import Flask, request, render_template, redirect, send_from_directory, abort, jsonify, session, url_for, Response, make_response
# from sqlalchemy import null
from test_code import *
from base_server import *
from route import *
from functools import wraps
from test_code.bug_calculate import *
from test_code.xmindupload import *
from test_code.to_xls import *
from werkzeug.utils import secure_filename
from xmindparser import xmind_to_xml
import platform
import json
from datetime import timedelta
from route_demo.views import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。
app.config['SESSION_COOKIE_NAME'] = 'login_auth'
re = Device_Manag()

bug = Mantis_Bug()
pp = Cha_Project()
bug_calculate = Bug_Calculate()
up = Xmind_Upload()
app.config.from_object('settings.DevConfig')

play = playMethods()
sp=serverPPTX()

'''
这里是注册蓝图
参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
即当request.url是以/monitor的情况下才会通过注册的蓝图的视图方法处理请求并返回
'''
app.register_blueprint(monitor, url_prefix='/monitor')
app.register_blueprint(route_demo, url_prefix='/route_demo')
app.register_blueprint(route_demo, url_prefix='/route_zll')

# 判断登录装饰器方法
def check_token(func):
    @wraps(func)
    def inner(*args, **kwargs):
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
# @check_permissions('/index')
def index():
    return render_template('index.html')


# 获取菜单目录
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    try:
        leven = session.get('username')[1]
    except:
        leven = 0
    menu = get_menu(leven)
    ret = {"code": 1000, "menu": menu}
    return json.dumps(ret)
    # return render_template('base.html', menu=menu)


# 2.登录
@app.route('/login_new', methods=['GET', 'POST'])
def login_new():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login = Login(username, password)
        data = login.valid_login()
        if data:
            session["username"] = data
            ret = {"Status": "ok", "Text": "登陆成功"}
            resp = Response(json.dumps(ret))
            resp.set_cookie('username', data[0])
            return resp
        else:
            ret = {"Status": "Erro", "Erro": "用户名密码不匹配"}
            return json.dumps(ret)
    else:
        if session.get('username'):
            return redirect('index')
        return render_template('login.html')


# 退出
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    data = session.get('username')
    if data is None:
        ret = make_response(redirect('login_new'))
        ret.delete_cookie('username')  # 清除cookies:username
    else:
        session.pop('username')  # 清除session
        ret = make_response(redirect('login_new'))
        ret.delete_cookie('username')  # 清除cookies:username
    return ret


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
# @check_permissions("/scheduling")
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
# @check_token
@check_permissions("/adddevice")
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
# @check_permissions("/device")
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
        return redirect("device")


# 修改使用状态
@app.route('/usestatus', methods=['post', 'get'])
# @check_token
@check_permissions("/usestatus")
def usestatus():
    if request.method == 'POST':
        devuser = request.get_data()
        devuser = json.loads(devuser.decode("utf-8"))
        devid = devuser['devid']
        user = devuser['user']
        re.appusep(devid, user)
        return "ok"


@app.route('/time_test', methods=['post', 'get'])
# @check_permissions("/time_test")
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
# @check_permissions('/bug_statistics')
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


# 自动化测试最新报告
@app.route('/appreport', methods=['post', 'get'])
def appwebreport():
    pt1 = APP_Report(1)
    pt2 = APP_Report(2)
    appdata = pt1.title_url(1,1)
    appreportlist = appdata[0]
    appnewreport = appdata[1]
    webdata = pt2.title_url(2,2)
    webreportlist = webdata[0]
    webnewreport = webdata[1]
    return render_template('appreport.html', appnewreport=appnewreport, appreportlist=appreportlist,webnewreport=webnewreport,webreportlist=webreportlist)

# APP更多报告列表
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
# @check_permissions("/project_information")
def Project_information():
    pp_rturn = request.args.get('firstname')
    data = pp.cha(pp_rturn)
    return render_template('project_information.html', u=data)
#卡车之家业务信息表-编辑
@app.route('/project_information_edit', methods=['POST', 'GET'])
# @check_permissions("/project_information")
def Project_information_edit():
    if request.method == 'GET':
        id = request.args.get('id')
        data = pp.cha_only(id)
        print(data)
        return render_template('project_information_edit.html', u=data)

    else:
        id = request.form.get('id')
        Business = request.form.get('Business')
        Product = request.form.get('Product')
        PM = request.form.get('PM')
        Business_type = request.form.get('Business_type')
        DMP = request.form.get('DMP')
        QD_Dev = request.form.get('QD_Dev')
        HD_Dev = request.form.get('HD_Dev')
        DEV_Leader = request.form.get('DEV_Leader')
        qa = request.form.get('qa')
        Platform = request.form.get('Platform')

        pp.edit(id,Business,Product,PM,Business_type,DMP,QD_Dev,HD_Dev,DEV_Leader,qa,Platform)
        data = pp.cha_only(id)

        return redirect('project_information')

#卡车之家业务信息表-新增
@app.route('/project_information_added', methods=['POST', 'GET'])
def Project_information_added():
    if request.method == 'GET':
        return render_template('project_information_added.html')

    else:
        id = request.form.get('id')
        Business = request.form.get('Business')
        Product = request.form.get('Product')
        PM = request.form.get('PM')
        Business_type = request.form.get('Business_type')
        DMP = request.form.get('DMP')
        QD_Dev = request.form.get('QD_Dev')
        HD_Dev = request.form.get('HD_Dev')
        DEV_Leader = request.form.get('DEV_Leader')
        qa = request.form.get('qa')
        Platform = request.form.get('Platform')

        pp.added(Business,Product,PM,Business_type,DMP,QD_Dev,HD_Dev,DEV_Leader,qa,Platform)
        return redirect("project_information")


# 接口监控-任务管理




# 抓虫节排行榜
@app.route('/grab_bug', methods=['post', 'get'])
# @check_permissions("/grab_bug")
def grab_bug():
    grab = Grab_Bug()
    data = grab.get_bug_score()
    return render_template('grab_bug.html', data=data)


# yapi页
@app.route('/yapi', methods=['get'])
# @check_permissions("/yapi")
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


# bug计算率页联动
@app.route('/selecttwo', methods=['post', 'get'])
def bug_selecttwo():
    if request.method == 'POST':
        project = request.form.get('project')
        pr = bug.get_pro_chi(project)
        return jsonify(pr)
    else:
        return null


# bug计算率页联动
@app.route('/selectthree', methods=['post', 'get'])
def bug_selectthree():
    if request.method == 'POST':
        proname = request.form.get('proname')
        vr = bug.get_version(proname)
        return jsonify(vr)
    else:
        return null


# bug计算率
@app.route('/bug_calculate', methods=['post', 'get'])
# @check_permissions("/bug_calculate")
def bug_calculate1():
    v = bug_calculate.countbug()
    vn = bug.get_pro()
    if request.method == 'POST':
        addtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        vname = request.form.get('project')
        proname = request.form.get('proname')
        versionname = request.form.get('versionname')
        name = request.form.get('name')
        checknum = request.form.get('checknum')
        fristnum = request.form.get('fristnum')
        leaknum = request.form.get('leaknum')
        newnum = request.form.get('newnum')
        bugcount = request.form.get('bugcount')
        # bug密度
        if float(checknum) == 0:
            bugdensity = 0
        else:
            bugdensity = '%.2f' % (float(bugcount) / float(checknum))
        # 首轮漏测率
        if float(bugcount) == 0:
            fristleak = 0
        else:
            fristleak = '%.2f' % (float(leaknum) / float(bugcount))
        # 引入错误率
        if float(fristnum) == 0 and float(leaknum) == 0:
            bringerror = 0
        else:
            bringerror = '%.2f' % (float(newnum) / (float(fristnum) + float(leaknum)))
        bug_calculate.bugInsert(vname, proname, versionname, name, checknum, fristnum, leaknum, newnum, bugcount,
                                bugdensity, fristleak, bringerror, addtime)
        data = bug_calculate.getInfor()
        return json.dumps(data)

    else:
        return render_template('bug_calculate.html', data=("", "", ""), vn=vn, v=v)


# bug率统计检查点
@app.route('/calculate', methods=['post', 'get'])
# @check_permissions("/calculate")
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
        return render_template('calculate.html', data=("", "", ""))


# bug率统计
@app.route('/calcu', methods=['post', 'get'])
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
        return render_template('calculate.html', data=("", "", ""))


#xmind上传下载
@app.route('/testcase',methods=['post','get'])
# @check_permissions('/testcase')
def upload():
    a = up.fileselect()
    if request.method == 'POST':
        f = request.files['file']
        up.fileupload(f)
        way = up.xmind_way()
        path = way+f.filename
        data = up.to_dict(path)
        print(data)
        up.fileinsert(f.filename,data)
        os.remove(path) 
        return "1"
    else:
        return render_template('upload.html',a = a)
 
#下载  
@app.route('/export_xls/<filename>', methods=['get'])
def return_file(filename):
    import os
    if request.method == "GET":
        search = up.xls_true(filename)
        if search:
            file_dir = os.path.join(up.xls_way(),filename)
        else:
            up.downexcel(filename)
            file_dir = os.path.join(up.xls_way(),filename)
        if os.path.isfile(file_dir):
            return send_from_directory(up.xls_way(), filename, as_attachment=True)
        abort(404)
#查询
@app.route('/selectfile', methods=['post','get'])
def select_file():
    if request.method == "POST":
        project = request.form.get('project')
        a = ""
        if(project == "全部"):
            a = up.fileselect()
        else:
            a = up.sel_file(project)
        return json.dumps(a)


# web更多报告列表
@app.route('/WebReport/<rpttime>', methods=['post', 'get'])
def webmorerpt(rpttime):
    url = "TestReport/%s" % (rpttime)
    return render_template(url)


@app.route('/arachni', methods=['get'])
def arachni():
    return redirect('http://127.0.0.1:9292')



# 以下为周报路由
@app.route('/weekly', methods=['post', 'get'])
def weekly():
    return app.send_static_file('html/weekly.html')


@app.route('/weekly_index', methods=['post', 'get'])
# @check_permissions("/time_test")
def weekly_index():

    return render_template('weekly_index.html')

#提交后就生成单独组的周报
@app.route('/subWeekly', methods=['post', 'get'])
def subWeekly():
    if request.method == 'POST':
        weekly = request.get_data()
        weekly = json.loads(weekly.decode("utf-8"))
        group_id = weekly['group']
        weekly=str(weekly).replace("\'","\\'")
        # weekly = request.get_data().decode("utf-8")
        # group_id=request.form.get('group')
        # print(group_id,weekly,type(weekly))
        data= sp.write_content(group_id,weekly)
        if data =="add succ":
            try:
                gen = generatePPTX(group_id)
                filename, defect = gen.generate_one()
            except Exception as e:
                ret = {"state": "0", "ms": str(e)}
                sp.update_status(group_id)
            else:
                ret = {"state": "1", "filename": filename}
        else:
            ret ={"state": "0", "ms": data}
        print(ret)
        return jsonify(ret)
    else:
        weekly = {"state":"0", "ms":"请使用post提交"}
        # weekly = {"state":"0", "ms":"小辉辉好"}
        return jsonify(weekly)

#生成技术中心周报
@app.route('/generate_all', methods=['post'])
def generate_all():
    if request.method == 'POST':
        try:
            gen = generatePPTX(0)
            filename,defect = gen.generate_one()
        except Exception as e:
            ret = {"state": "0", "ms": str(e)}
        else:
            if defect==[]:
                ret = {"state": "1", "filename": filename,"defect":defect}
            else:
                ret = {"state": "2", "filename": filename,"defect":defect}
        return jsonify(ret)


@app.route('/download_pptx/<filename>',methods=['get'])
def download_pptx(filename):
    print(filename)
    if request.method == "GET":
        way = "ppt/pptx/"
        file_dir = os.path.join(way, filename)
        print(way,filename)
        if os.path.isfile(file_dir):
            return send_from_directory(way, filename, as_attachment=True)
        else:
            abort(404)



@app.route('/upimg',methods=['post'])
def upimg():
    r = {"state":"0", "ms":"失败"}
    if request.method == 'POST':
        f = play.imgUp(request.files['file'])
        r = {"state":"1", "ms":"成功","imgname":f}

    return jsonify(r)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
