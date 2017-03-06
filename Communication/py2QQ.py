# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import hashlib
from urllib import request,parse
from http import cookiejar
import re,random,time
import threading as th
import json.encoder as json_encode
import json.decoder as json_decode


class QQ(object):
    """
     Login QQ
    """
    def __init__(self):
        self.__headers ={
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.9 Safari/534.30',\
                        'Referer':'http://ui.ptlogin2.qq.com/cgi-bin/login?target=self&style=5&mibao_css=m_webqq&appid=1003903&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fwebqq.qq.com%2Floginproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20110909003'\
                        }
        self.__cookiepath = 'C:\\Users\\dingyangfan\\Desktop\php\\tt.txt'
        self.__qq = None
        self.__pswd = None
        self.__verifycode = None
        self.__clientid = 21628014
        self.__http = {}
        self.__psessionid = ''
        self.__ptwebqq = ''
        self.__vfwebqq = ''
        self.__skey = ''
        self. __poll2 = None
        self.__get_msg_tip = None
        self.__rc = 0
        self.__send_num = 31330000
        self.httpproess()
        self.__Login()
        pass

    def __preprocess(self,password,verifycode):
        """
            QQ密码加密部份
        """
        return hashlib.md5( (self.__md5_3((password).encode('utf-8')) + (verifycode).upper()).encode('utf-8')).hexdigest().upper()
        pass

    def __md5_3(self,str):
        """
            QQ密码md5_3部份
        """
        return hashlib.md5(hashlib.md5(hashlib.md5(str).digest()).digest()).hexdigest().upper()
        pass

    def httpproess(self):
        """
            初始化模拟进程
        """
        self.__http['cj'] = cookiejar.MozillaCookieJar(self.__cookiepath)
        self.__http['opener'] = request.build_opener(request.HTTPCookieProcessor(self.__http['cj']))
        return self.__http
        pass

    def __request(self, url, method='GET', data={}, savecookie=False):
        """
            请求url
        """
        if (method).upper() == 'POST':
            data = parse.urlencode(data).encode('utf-8')
            self.__http['req'] = request.Request(url, data, self.__headers)
        else:
            self.__http['req'] = request.Request(url=url, headers=self.__headers)
        fp = self.__http['opener'].open(self.__http['req'])
        try:
            strs = fp.read().decode('utf-8')
        except UnicodeDecodeError:
            strs = fp.read()
        if savecookie == True:
            self.__http['cj'].save(ignore_discard=True,ignore_expires=True)
        fp.close()
        return strs
        pass

    def __getcookies(self,name):
        fp = open(self.__cookiepath)
        fp.seek(130)
        for read in fp.readlines():
            str = read.split(name)
            if len(str) == 2:
                fp.close()
                return str[1].strip()
        fp.close()
        return None
        pass

    def __getverifycode(self):
        """
            @url:http://ptlogin2.qq.com/check?uin=644826377&appid=1003903&r=0.56373973749578
        """
        urlv = 'http://ptlogin2.qq.com/check?uin='+ ('%s' % self.__qq)+'&appid=1003903&r='+ ('%s' % random.Random().random())
        str = self.__request(url=urlv, savecookie=True)
        str = re.findall(r'\d|(?<=\')[a-zA-Z0-9\!]{4}',str)
        return str
        pass

    def __request_login(self):
        """
            @url:http://ptlogin2.qq.com/login
            @params:{u:644826377
                    p:73DA5C1145E0F82247F60B3A17B89E6A   verifycode:!S10   webqq_type:10
                    remember_uin:1  login2qq:1  aid:1003903  u1:http://webqq.qq.com/loginproxy.html?login2qq=1&webqq_type=10
                    h:1  ptredirect:0   ptlang:2052  from_ui:1   pttype:1  dumy:
                    fp:loginerroralert   action:1-24-62651  mibao_css:m_webqq}
        """
        urlv = 'http://ptlogin2.qq.com/login?u='+('%s' %  self.__qq) +'&' +  'p=' + ('%s' % self.__pswd) +  '&verifycode='+ ('%s' % self.__verifycode[1]) +'&remember_uin=1&aid=1003903' +  "&u1=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html%3Fstrong%3Dtrue" +  '&h=1&ptredirect=0&ptlang=2052&from_ui=1&pttype=1&dumy=&fp=loginerroralert'
        str = self.__request(url = urlv,savecookie=True)
        if str.find('登录成功') != -1:
            #执行二次登录
            self.__ptwebqq = self.__getcookies('ptwebqq')
            self.__skey = self.__getcookies('skey')
            self.__request_post()
        elif str.find('不正确') != -1:
            print('你输入的帐号或者密码不正确，请重新输入。')
        else:
            print('登录失败')
        pass

    def __request_post(self):
        '''
            http://d.web2.qq.com/channel/login2
            r:{"status":"online","ptwebqq":"95b148b95af9be7677757b3a629e3904f52f153d0b714c527f81f8d9e385867a","passwd_sig":"",
            "clientid":"21628014","psessionid":null}
            clientid:21628014
            psessionid:null
        '''
        self.__headers.update({'Referer':'http://d.web2.qq.com/proxy.html?v=20110331002&callback=2'})
        a = {'status':'online','ptwebqq':self.__getcookies('ptwebqq'),'passwd_sig':'','clientid':self.__clientid,'psessionid':'null'}
        array = {'r':json_encode.JSONEncoder().encode(a),'clientid':self.__clientid,'psessionid':'null'}
        url = 'http://d.web2.qq.com/channel/login2'
        str = self.__request(url,'POST',array)
        str = json_decode.JSONDecoder().decode(str)
        self.__psessionid = str['result']['psessionid']
        self.__vfwebqq = str['result']['vfwebqq']
        self.__get_friend_info2()
        self.__get_user_friends2()
        self.__get_group_name_list_mask2()
        self.__poll2_()
        self.__get_msg_tip_()
        pass

    def __poll2_(self):
        """
            不知道干嘛的，一分钟连接一次，属于长连接，接收消息
            @url:http://d.web2.qq.com/channel/poll2
            r:{"clientid":"9467930","psessionid":"8368046764001e636f6e6e7365727665725f77656271714031302e3132382e36362e31313500003058000000c0026e040009456f266d0000000a407169446b464737436b6d00000028f8d256743e5c191cb40a2217845fab12fda62acd2e6145ae196976d7a8b3bb11a64d3c9565868322","key":0,"ids":[]}
            clientid:9467930
            psessionid:8368046764001e636f6e6e7365727665725f77656271714031302e3132382e36362e31313500003058000000c0026e040009456f266d0000000a407169446b464737436b6d00000028f8d256743e5c191cb40a2217845fab12fda62acd2e6145ae196976d7a8b3bb11a64d3c9565868322
        """
        self.__headers.update({'Referer':'http://d.web2.qq.com/proxy.html?v=20110331002&callback=2'})
        urlv = 'http://d.web2.qq.com/channel/poll2'
        a = {'clientid':self.__clientid,'psessionid':self.__psessionid,'key':0,'ids':[]}
        array = {'r':json_encode.JSONEncoder().encode(a),'clientid':self.__clientid,'psessionid':self.__psessionid}
        self.__poll2 = self.__request(url = urlv,method='POST',data = array)
        str = json_decode.JSONDecoder().decode(self.__poll2)
        print(str)
        if str['retcode'] == 0:
            if str['result'][0]['poll_type'] == 'message':
                self.__message(str['result'][0]['value']['from_uin'])
            elif str['result'][0]['poll_type'] == 'group_message':
                self.__group_message(str['result'][0]['value']['from_uin'])
                pass
        t1 = th.Timer(1,self.__poll2_)
        t1.start()
        pass

    def __get_msg_tip_(self):
        """
            #也不知道是什么，反正一直请求
            @url:http://webqq.qq.com/web2/get_msg_tip?uin=&tp=1&id=0&retype=1&rc=64&lv=2&t=1315746772886
        """
        self.__headers.update({'Referer':'http://webqq.qq.com/'})
        self.__rc += 1
        num = 100 + self.__rc
        t = '%s' % '%d' % time.time() + '%s' % num
        urlv = 'http://webqq.qq.com/web2/get_msg_tip?uin=&tp=1&id=0&retype=1&rc='+'%s'% self.__rc +'&lv=3&t=' + t
        self.__get_msg_tip = self.__request(urlv)
        print(self.__get_msg_tip)
        t2 = th.Timer(60,self.__get_msg_tip_)
        t2.start()
        pass

    def __get_friend_info2(self):
        '''
            @url:http://s.web2.qq.com/api/get_friend_info2?tuin=self.__qq&verifysession=&code=&vfwebqq=self.__vfwebqq
        '''
        self.__headers.update({'Referer':'http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=2'})
        url = 'http://s.web2.qq.com/api/get_friend_info2?tuin='+ self.__qq + '&verifysession=&code=&vfwebqq=' + self.__vfwebqq + '&t=%s' % '%d' % time.time() + '100'
        str = self.__request(url)
        print(str)
        pass

    def __get_user_friends2(self):
        '''
            @url:http://s.web2.qq.com/api/get_user_friends2
        '''
        self.__headers.update({'Referer':'http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=2'})
        url = 'http://s.web2.qq.com/api/get_user_friends2'
        a = {'h':'hello','vfwebqq':self.__vfwebqq}
        array = {'r':json_encode.JSONEncoder().encode(a)}
        str = self.__request(url,'POST',array)
        print(str)
        pass

    def __get_group_name_list_mask2(self):
        '''
            @url:http://s.web2.qq.com/api/get_group_name_list_mask2
        '''
        self.__headers.update({'Referer':'http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=2'})
        url = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
        a = {'vfwebqq':self.__vfwebqq}
        array = {'r':json_encode.JSONEncoder().encode(a)}
        str = self.__request(url,'POST',array)
        print(str)
        pass

    def __send_message(self,uid,msg):
        '''
            @url:http://d.web2.qq.com/channel/send_buddy_msg2
            r:{"to":3023379661,"face":180,"content":"[\"哈哈\",\"\\n【提示：此用户正在使用WebQQ：http://webqq.qq.com/】\",[\"font\",               {\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]","msg_id":31330001,"clientid":"76133590",                    "psessionid":"s"}
                clientid:76133590
                psessionid:s

            Referer:http://d.web2.qq.com/proxy.html?v=20110331002&callback=2
            {"retcode":0,"result":"ok"}
        '''
        self.__send_num +=1
        msg = "[\""+ msg +"\",[\"font\",{\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]"
        self.__headers.update({'Referer':'http://d.web2.qq.com/proxy.html?v=20110331002&callback=2'});
        url = 'http://d.web2.qq.com/channel/send_buddy_msg2'
        a = {'to':uid,'face':180,'content':msg,'msg_id':self.__send_num,'clientid':self.__clientid,'psessionid':self.__psessionid}
        array = {'r':json_encode.JSONEncoder().encode(a),'clientid':self.__clientid,'psessionid':self.__psessionid}
        str = self.__request(url,'POST',array)
        print(str)
        pass

    def __message(self,uid):
        '''
            {"retcode":0,"result":[{"poll_type":"message","value":{"msg_id":13013,"from_uin":3023379661,"to_uin":644826377,"msg_id2":503935,"msg_type":9,"reply_ip":176752345,"time":1316143960,"content":[["font",{"size":13,"color":"000000","style":[0,0,0],"name":"\u5B8B\u4F53"}],"\u4E0D\u662F\u5427\u3002"]}}]}

        '''
        self.__send_message(uid,'我是机器人%s' % time.time())
        pass

    def __send_group_message(self,gid,msg):
        '''
            @url:http://d.web2.qq.com/channel/send_qun_msg2
            r:{"group_uin":1132101900,"content":"[\"哈哈哈，测试\",\"\\n【提示：此用户正在使用WebQQ：http://webqq.qq.com/】\",[\"font\",           {\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]","msg_id":31330002,"clientid":"76133590",
            "psessionid":"a"}
            clientid:76133590
            psessionid:a

            Referer:http://d.web2.qq.com/proxy.html?v=20110331002&callback=2

            {"retcode":0,"result":"ok"}
        '''
        self.__send_num +=1
        msg = "[\"" +msg + "\",[\"font\",{\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]"
        self.__headers.update({'Referer':'http://d.web2.qq.com/proxy.html?v=20110331002&callback=2'});
        url = 'http://d.web2.qq.com/channel/send_qun_msg2'
        a = {'group_uin':gid,'content':msg,'msg_id':self.__send_num,'clientid':self.__clientid,'psessionid':self.__psessionid}
        array = {'r':json_encode.JSONEncoder().encode(a),'clientid':self.__clientid,'psessionid':self.__psessionid}
        str = self.__request(url,'POST',array)
        print(str)
        pass

    def __group_message(self,gid):
        '''
            {"retcode":0,"result":[{"poll_type":"group_message","value":{"msg_id":8044,"from_uin":1132101900,"to_uin":644826377,"msg_id2":178306,"msg_type":43,"reply_ip":2886742214,"group_code":317106137,"send_uin":3023379661,"seq":10654,"time":1316143836,"info_seq":32946855,"content":[["font",{"size":13,"color":"000000","style":[0,0,0],"name":"\u5B8B\u4F53"}],"\u5DE5"]}}]}

        '''
        self.__send_group_message(gid,'我是机器人%s' % time.time())
        pass

    def __Login(self):
        """
            qq登录
        """
        self.__qq = "3285670383"  # input('QQ号：')
        self.__pswd = "85828731vic"  # input('QQ密码：')
        self.__qq = self.__qq.strip()
        self.__pswd = self.__pswd.strip()
        self.__verifycode = self.__getverifycode()
        self.__pswd = self.__preprocess(self.__pswd,  '%s' % self.__verifycode[1])
        self.__request_login()
        pass

s = QQ()