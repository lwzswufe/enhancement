# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


class send_email(object):
    def __init__(self, config_file='D:\\Python_Config\\Email_Send.json'):
        config = json.load(open(config_file, 'r'))
        self.sender = config['sender']
        self.smtpserver = config['smtpserver']
        self.username = config['username']
        self.password = config['password']

    def sends(self, receiver=["3285670383@qq.com"], title=u"邮箱提示系统",
             context="Hi!\nHow are you?\nI write this email to python"):
        for receiver_email in receiver:
            self.send(receiver_email, title, context)

    def send(self, receiver=["3285670383@qq.com"], title="Im Lwz",
             context="Hi!\nHow are you?\n"):
        # Create message container - the correct MIME type is multipart/alternative.
        if len(receiver) > 1:
            msg = MIMEMultipart('multipart')
        else:
            msg = MIMEMultipart('alternative')
            receiver = receiver[0]
        msg['Subject'] = title
        msg.attach(MIMEText(context, 'plain'))
        # Create the body of the message (a plain-text and an HTML version).
        msg['from'] = self.sender
        msg['to'] = receiver

        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, receiver, msg.as_string())
        smtp.quit()
        print('email send to ', receiver, 'successful')


if __name__ == '__main__':
    se = send_email()
    se.send()
    se.sends(receiver=["3285670383@qq.com", "lwzswufe@163.com"])