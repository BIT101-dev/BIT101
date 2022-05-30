'''
Author: flwfdd
Date: 2022-05-29 16:15:53
LastEditTime: 2022-05-30 02:32:19
Description: 发送邮件
_(:з」∠)_
'''
import smtplib
from email.mime.text import MIMEText

import config



def send(to,title,msg):
    message=MIMEText(msg,'html','utf-8')
    message['Subject']=title
    message['To']=to
    message['From']=config.mail_user
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(config.mail_host)
        smtpObj.login(config.mail_user,config.mail_pass) 
        smtpObj.sendmail(
            config.mail_user,to,message.as_string()) 
        smtpObj.quit() 
        return True
    except smtplib.SMTPException as e:
        print(e)
        return False