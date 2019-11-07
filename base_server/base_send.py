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
        msg['to'] = str(receiver)[1:-1].replace("'","")
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

if __name__ == '__main__':
    S=Send_All()
    S.sending("https://oapi.dingtalk.com/robot/send?access_token=65480cb93c4aa8019f1d2c6434baef52743cc050cd04e7ff1d10aa11e5835e1c","ceshi")

