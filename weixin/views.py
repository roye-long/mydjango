# -*- coding: utf8 -*-
from django.http import HttpResponse
import hashlib, time, re,json,sys
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree
import StringIO
WEIXIN_TOKEN = 'weixin'
# Create your views here.

def weixin(request):  
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        if signature != None:
            token = WEIXIN_TOKEN
            tmp_list = [token, timestamp, nonce]
            tmp_list.sort()
            tmp_str = "%s%s%s" % tuple(tmp_list)
            tmp_str = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()
            if tmp_str == signature:
                return HttpResponse(echostr)
        else:
            return HttpResponse("Error")
    else:
        request_xml = ElementTree.fromstring(request.body)
        fromUser = request_xml.find('ToUserName').text
        toUser = request_xml.find('FromUserName').text
        msgtype = request_xml.find('MsgType').text
        nowtime = str(int(time.time()))
        if msgtype == 'text':
            content = request_xml.find('Content').text
            if content == '帮助':
                message = 'subscribe'
            elif content == '【收到不支持的消息类型，暂无法显示】':
                message = '收到动态表情'
            else:
                message = '收到文本消息'
        elif msgtype == 'location':
            label = request_xml.find('Label').text
            message = (u'收到位置信息：') + label
        elif msgtype == 'image':
            message = (u'收到图片')
        elif msgtype == 'voice':
            message = (u'收到语音')
        elif msgtype == 'shortvideo':
            message = (u'收到短视频')
        elif msgtype == 'link':
            message = (u'收到链接')
        elif msgtype == 'event':
            event = request_xml.find('Event').text
            if event == 'subscribe':
                message = 'subscribe'
        return render(request,'text.xml',{'toUser': toUser, 'fromUser': fromUser, 'nowtime': nowtime, 'content': message})

