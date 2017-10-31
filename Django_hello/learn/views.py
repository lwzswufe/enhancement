from django.shortcuts import render
from django.http import HttpResponse
'''
引入HttpResponse，它是用来向网页返回内容的，就像Python中的
print 一样，只不过 HttpResponse 是把内容显示到网页上。
我们定义了一个index()函数，第一个参数必须是 request，
与网页发来的请求有关，request 变量里面包含get或post的内容，
用户浏览器，系统等信息在里面（后面会讲，先了解一下就可以）。

函数返回了一个 HttpResponse 对象，可以经过一些处理，
最终显示几个字到网页上。
'''
def index(request):
    return HttpResponse(u"学习Django!")