# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email import encoders
import json


class send_email(object):
    def __init__(self, config_file='D:\\Python_Config\\Email_Send_Standard.json'):
        config = json.load(open(config_file, 'r', encoding='utf-8'))
        self.sender = config['sender']
        self.smtpserver = config['smtpserver']
        self.username = config['username']
        self.password = config['password']
        self.fname = config['fname']
        self.refname = config['refname']
        self.htmlfile = config['htmlfile']
        self.receiver_file = config['receiver']
        self.receivers = list()
        self.get_receiver()
        self.msg = []

    def sends(self, receiver=["3285670383@qq.com"], title=u"邮箱提示系统",
             context=""):
        for receiver_email in receiver:
            self.send_standard(receiver_email, title, context)

    def send(self, receiver=["3285670383@qq.com"], title="Im Lwz",
             context="Hi!\nHow are you?\n"):
        # Create message container - the correct MIME type is multipart/alternative.
        if len(receiver) > 1:
            self.msg = MIMEMultipart('multipart')
        else:
            self.msg = MIMEMultipart('alternative')
            receiver = receiver[0]
        self.msg['Subject'] = title

        self.msg.attach(MIMEText(context, 'plain'))
        # Create the body of the message (a plain-text and an HTML version).

        self.msg['from'] = self.sender
        self.msg['to'] = receiver

        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, receiver, self.msg.as_string())
        smtp.quit()
        print('email send to ', receiver, 'successful')

    def send_standard(self, receiver=["3285670383@qq.com"], title="Im Lwz",
             context=""):
        # Create message container - the correct MIME type is multipart/alternative.
        if len(receiver) > 1:
            self.msg = MIMEMultipart('multipart')
        else:
            self.msg = MIMEMultipart('alternative')
            receiver = receiver[0]
        self.msg['Subject'] = title

        # self.msg.attach(MIMEText(context, 'plain'))
        # Create the body of the message (a plain-text and an HTML version).
        with open(self.htmlfile, 'r') as f:
            html_text = f.read()

        self.msg.attach(MIMEText(html_text, 'html', 'utf-8'))

        for i in range(len(self.fname)):
            self.add_attachment(i)

        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, receiver, self.msg.as_string())
        smtp.quit()
        print('email send to ', receiver, 'successful')

    def add_pic(self, fname, refname, pic_id):
        with open(fname, 'rb') as f:
            #  设置附件的MIME和文件名，这里是jpg类型:
            mime = MIMEBase('image', 'jpg', filename=refname)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=refname)
            mime.add_header('Content-ID', '<' + str(pic_id) + '>')
            mime.add_header('X-Attachment-Id', str(pic_id))
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            self.msg.attach(mime)

    def add_attachment(self, id):
        if self.refname[id][-4:] == '.jpg':
            pass
            # self.add_pic(self.fname[id], self.refname[id], id)
        else:
            with open(self.fname[id], 'rb') as f:
                context = f.read()
                if context:
                    part = MIMEApplication(context)
                    part.add_header('Content-Disposition', 'attachment', filename=self.refname[id])
                    self.msg.attach(part)
                else:
                    print('empty file:', self.fname[id])

    def get_receiver(self):
        with open(self.receiver_file, "r") as f:
            context = f.read()
        for line in context.split('\n'):
            if line.find('@') > 0:
                self.receivers.append(line)

if __name__ == '__main__':
    se = send_email()
    se.sends(receiver=["lwzswufe@126.com"], context='', title="缠论股票短线信号")
    # se.send_standard(context='', title="缠论股票短线信号")
                     # receiver='gj706@163.com')
    # se.sends(receiver=["3285670383@qq.com", "lwzswufe@163.com"])