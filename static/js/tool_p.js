    //
    function loadXMLDoc(e){
        var td = e.parentNode.previousElementSibling;
        var value = td.querySelector('div').innerHTML;
        var url_id = td.querySelector('div').getAttribute('value');
        // console.log(value)
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        if (value == 0)
        {
            value = 1
        }
        else
        {
            value = 0
        }
        var data ='{ "status" :'+ value +', "url_id" : ' + url_id + '}';
        xmlhttp.open("POST","test_ajax",true);
        xmlhttp.send(data);
        xmlhttp.onreadystatechange = function()
        {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200 ) 
            {
            if (xmlhttp.responseText == 'ok')
            {
              location.reload();
            }
            else
            {
              alert('请求出错，请重试')
            }
          // document.getElementById("test_button").innerHTML = xmlhttp.responseText
          }
        }
    }

    function del(e) {
        if (window.confirm("确定要删除吗")) {
            var td = e.parentNode.previousElementSibling;
            var url_id = td.querySelector('div').getAttribute('value');
            var xmlhttp;
            xmlhttp = new XMLHttpRequest();
            var data = '{ "status" : ' + 2 + ', "url_id" : ' + url_id + '}';
            xmlhttp.open("POST", "test_ajax", true);
            xmlhttp.send(data);
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    if (xmlhttp.responseText == 'ok') {
                        location.reload();
                    } else {
                        alert('请求出错，请重试')
                    }
                    // document.getElementById("test_button").innerHTML = xmlhttp.responseText
                }
            }
        }
    }

    function edit1(e) {
        var td = e.parentNode.previousElementSibling;
        var url_id = td.querySelector('div').getAttribute('value');
        window.location.href="http://127.0.0.1:5000/editapi?url_id="+url_id
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        var data ='{  "url_id" :' + url_id + '}';
        xmlhttp.open("GET","editapi",true);
        xmlhttp.send(data);
        xmlhttp.onreadystatechange = function()
        {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200 )
            {
            alert(h)
            }
        }
    }
    
    //test
    function loadXMLDoc1()
        {
        var xmlhttp;
        if (window.XMLHttpRequest)
            {
            xmlhttp=new XMLHttpRequest();
            }
        xmlhttp.onreadystatechange=function()
        {
            if (xmlhttp.readyState==4 && xmlhttp.status==200)
            {
            document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
            }
        }
        xmlhttp.open("POST","test_ajax",true)
        x = document.getElementById("abc").innerHTML;
        var v
        xmlhttp.send("v="+x)
    }
    
    //生成左侧已有项目列表
    function get_list(){
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET","ajax_get_list",true);
        xmlhttp.send();
        xmlhttp.onreadystatechange = function()
        {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200 ) 
            {
            var c = JSON.parse(xmlhttp.responseText)
            var ele = ''
            for (var i in c)
                {
                ele = ele + "<li><a href=" + c[i] + " title=" + i + " style='color:#A1A9B3'>" + i +"</a></li>"
                }
            }
            document.getElementById('list').innerHTML=ele
        }
    }

    //删除任务
    function deltask(e) {
        if(window.confirm("确定要删除吗,删除之后此任务下所有接口都将被删除？"))
        {
            var td = e.parentNode.previousElementSibling;
            var task_id = td.querySelector('div').getAttribute('value');
            var xmlhttp;
            xmlhttp = new XMLHttpRequest();
            var data = '{ "status" : ' + 2 + ', "task_id" : ' + task_id + '}';
            xmlhttp.open("POST", "EditTaskStatus", true);
            xmlhttp.send(data);
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    if (xmlhttp.responseText == 'ok') {
                        location.reload();
                    } else {
                        alert('请求出错，请重试')
                    }
                    // document.getElementById("test_button").innerHTML = xmlhttp.responseText
                    }
                }
            }
        }

    //启用关闭任务
    function loadXMLDocTask(e){
        var td = e.parentNode.previousElementSibling;
        var value = td.querySelector('div').innerHTML;
        var task_id = td.querySelector('div').getAttribute('value');
        // console.log(value)
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        if (value == 0)
            {
              value = 1
            }
            else
            {
              value = 0
            }
        var data ='{ "status" :'+ value +', "task_id" : ' + task_id + '}';
        xmlhttp.open("POST","EditTaskStatus",true);
        xmlhttp.send(data);
        xmlhttp.onreadystatechange = function()
        {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200 )
                {
                if (xmlhttp.responseText == 'ok')
                {
                    location.reload();
                }
                else
                {
                    alert('请求出错，请重试')
                }
          // document.getElementById("test_button").innerHTML = xmlhttp.responseText
            } 
        }
    }


    /*编辑设备*/
    function editdev(e){
        window.location.href="http://192.168.1.59:5000/editdev?devid="+e.dataset.id
    }

    //删除设备
    function deldev(e){
        var devid = e.dataset.id;
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        var data ='{ "status" : '+ 1 +', "devid" : ' + devid + '}';
        xmlhttp.open("POST","deldev",true);
        xmlhttp.send(data);
        xmlhttp.onreadystatechange = function()
        {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200 ) 
                {
                if (xmlhttp.responseText == 'ok')
                {
                  location.reload();
                }
                else
                {
                  alert('请求出错，请重试')
                }
            }
        }
    }


    function lc(e){
        if (e.classList.contains('disabled')) {
            return
        }
        document.getElementById('loading').style.display='';
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        // {#var data ='{  "url_id" :' + url_id + '}';#}
        xmlhttp.open("POST","login",true);
        xmlhttp.send();
        setTimeout(function(){
            document.getElementById("oImg").src = "/static/pic/QR.png";
            document.getElementById('oImg').style.display = "block";
            document.getElementById('loading').style.display = "none";
        },3000)
        btn[1].classList.remove('disabled');
        xmlhttp.onreadystatechange = function(){
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
                var c = JSON.parse(xmlhttp.responseText)
                if(c.code==1000){
                    alert("登陆成功！")
                    document.getElementById("oImg").src = "";
                    for (let i = 0; i < btn.length; i++) {
                        if (btn[i].classList.contains('disabled')){
                            btn[i].classList.remove('disabled')
                        } else{
                             btn[i].classList.add('disabled')
                        }
                    }
                }
            }
        }
    }
    

    function refurbish(e){
        if (e.classList.contains('disabled')) {
            return
        }
        var img_src="/static/pic/QR.png?"+Math.random()
        document.getElementById("oImg").src = img_src;
    } 


    function  ec(e){
        if (e.classList.contains('disabled')) {
                return
            }
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        // {#var data ='{  "url_id" :' + url_id + '}';#}
        xmlhttp.open("POST","exit",true);
        xmlhttp.send();
        xmlhttp.onreadystatechange = function()
        {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200 )
            {
            location.reload()

            }
        }
    }

    
    function  statistic(e){
        if (e.classList.contains('disabled')) {
                return
            }
        document.getElementById('loading').style.visibility='hidden';

        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        // {#var data ='{  "url_id" :' + url_id + '}';#}
        xmlhttp.open("POST","statistic",true);
        xmlhttp.send();

        xmlhttp.onreadystatechange = function()
        {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200 )
            {
            var c = JSON.parse(xmlhttp.responseText)
                // {#alert(c.code)#}
                if (c.code == 1001){
                    alert("未登录")
                }else {
                // {#var obj = JSON.parse(xmlhttp.responseText)#}
                // {#var data=obj['city']#}
                    btn[1].classList.add('disabled')
                    btn[2].classList.add('disabled')
                    document.getElementById("oImg").src =""
                    optionsex.series[0].data= c.sex
                    optioncity.series[0].data=c.Province
                    myCharsex.setOption(optionsex);
                    myCharcity.setOption(optioncity);
                }
            }
        }
    }


    function  wc(e) {
        if (e.classList.contains('disabled')) {
            return
        }
        var img_RemarkName="/static/pic/RemarkName.png?"+Math.random()
        document.getElementById("RemarkName").src = img_RemarkName;
        // {#document.getElementById("RemarkName").src = "/static/pic/RemarkName.png";#}
        document.getElementById('RemarkName').style.display = "block";
    }


    function devtype(e){
        var devtype = e.dataset.id;
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        var data ='{ "devtype" : '+ devtype +'}';
        xmlhttp.open("POST","typedev",true);
        xmlhttp.send(data);
        xmlhttp.onreadystatechange = function()
        {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200 ) 
            {
            document.getElementById("123").innerHTML=xmlhttp.responseText
            }
        }
    }


