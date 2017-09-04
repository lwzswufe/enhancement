# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import itchatmp
from itchatmp.content import  *
import urllib.request as request
import json
from MediaPlatform import wechat_reply


class send_message_to_wechat(object):
    def __init__(self, config_file='D:\\Python_Config\\WeChatMediaPlatform.json'):
        config = json.load(open(config_file, 'r', encoding="utf-8"))
        self.is_test = False
        self.appid = config['appid']
        self.app_secret = config['app_secret']
        self.token = ''
        self.reply = wechat_reply.auto_reply()

        @itchatmp.msg_register(itchatmp.content.TEXT)
        def text_reply(msg):
            return msg['Content']
            # return self.reply.reply_signal(msg)

    def get_token(self):
        fn = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential' \
             '&appid={appid}&secret={secret}'.format(appid = self.appid, secret=self.app_secret)
        # self.token = itchatmp.access_token(fn)
        resp = request.urlopen(fn)
        text = str(resp.read()).split('"')
        if text[1] == 'access_token':
            self.token = text[3]
        elif text[1] == 'errcode':
            print('get token failed')
            raise(Exception)
        else:
            print('get unknown resp')
            raise (Exception)

    def wechat_login(self):                        # 自动登陆微信
        self.get_token()
        if self.is_test:
            print(u'本地测试开启')
            itchatmp.update_config(itchatmp.WechatConfig(
                token=self.token,
                appId=self.appid,
                appSecret=self.app_secret))
        else:
            itchatmp.update_config(itchatmp.WechatConfig(
                token=self.token,
                appId=self.appid,
                appSecret=self.app_secret))
            print(u'微信登陆成功')
            itchatmp.set_logging(loggingLevel=10)

            @itchatmp.msg_register(itchatmp.content.TEXT)
            def text_reply(msg):
                return msg['Content']


if __name__ == '__main__':
    sw = send_message_to_wechat()
    sw.wechat_login()
    itchatmp.run()# 扫描二维码并登陆
