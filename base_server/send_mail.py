#encoding:utf-8
import smtplib
import email.mime.text
import email.mime.multipart

# #发邮件
class Send_Email():

    def sendemail(self,receiver,content):
        sender = 'mantis@360che.com'
        smtpserver = 'smtp.mxhichina.com'

        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = sender
        msg['to'] = receiver
        msg['subject'] = "接口异常报警通知"

        txt = email.mime.text.MIMEText(content)
        msg.attach(txt)

        smtp = smtplib.SMTP()
        smtp.connect('smtp.mxhichina.com','25' )
        smtp.login('mantis@360che.com', '360CHEche1')
        smtp.sendmail(sender, receiver, str(msg))
        smtp.quit()

# aa = Send_Email()
# aa.sendemail(["leileiz.zhang@360che.com","jinyue.cui@360che.com"],"金月是猪")
