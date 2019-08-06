# encoding:utf-8
import smtplib
import email.mime.text
import email.mime.multipart
import json
import requests


# 发邮件、发钉钉
class Send_All():

    # 发邮件
    def sendemail(self, receiver, content):
        sender = 'mantis@360che.com'
        smtpserver = 'smtp.mxhichina.com'

        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = sender
        msg['to'] = str(receiver)
        msg['subject'] = "接口异常报警通知"

        txt = email.mime.text.MIMEText(content)
        msg.attach(txt)

        smtp = smtplib.SMTP()
        smtp.connect('smtp.mxhichina.com', '25')
        smtp.login('mantis@360che.com', '360CHEche1')
        smtp.sendmail(sender, receiver, str(msg))
        smtp.quit()

    # 发钉钉
    def sending(self, token, content):
        HEADERS = {"Content-Type": "application/json ;charset=utf-8 "}
        data = {"msgtype": "text", "text": {"content": content}, "at": {"atMobiles": [], "isAtAll": "false"}}
        data = json.dumps(data)
        res = requests.post(token, data=data, headers=HEADERS)