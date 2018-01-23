# -*- coding:utf-8 -*-
import datetime,json
from django.http import HttpResponse
from django.db.models import  *
from django.shortcuts import render ,render_to_response
from myapp.models import  Jd,Newline
from ocr2 import OCR
from PIL import Image
import io,base64
from django import forms
import qrcode
from cStringIO import StringIO
import requests
from time import time, sleep
from random import random
import urllib
from io import BytesIO
import pyexcel as pe
import unicodecsv as csv
import re
# Create your views here.
def sayHello(request):
   ''' s = 'Hello World!'
    current_time = datetime.datetime.now()
    html = '<html><head></head><body><h1> %s </h1><p> %s </p></body></html>' % (s, current_time)
    return HttpResponse(html)'''
   #list = Jd.objects.all()
   list=Jd.objects.values('color').annotate(ct=Count('color'))
   content={"list":list}
   return render(request, 'index.html', content)
def linelook(request):
    list = Jd.objects.values('color').annotate(ct=Count('color'))
    cont=[]
    for ave in list:
        cont.append(ave)
    content = {"list": json.dumps(cont)}
    return render_to_response('line.html', content)
def line2look(request):
    indexlist = ['one', 'tow', 'three', 'four', 'five', 'six', 'seven']
    mxdatalist = [11, 11, 15, 13, 12, 13, 10]
    midatalist = [1, -2, 2, 5, 3, 2, 0]
    for i in range(len(indexlist)):
        Newline.objects.get_or_create(xinqi=indexlist[i], maxs=mxdatalist[i], minx=midatalist[i])
    list = Newline.objects.values("xinqi","maxs","minx")
    cont = []
    for ave in list:
        cont.append(ave)
    content = {"list": json.dumps(cont)}
    return render_to_response('line1.html', content)
class UserForm(forms.Form):
    headImg = forms.FileField()
def ocr(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            ocr=OCR('/root/chaoguo.long/mydjango/svm_model.txt')
            if 'headImg' in request.FILES:
                Img = request.FILES['headImg']
                byteImag = base64.b64encode(Img.read())
                img=base64.b64decode(byteImag)
                image = Image.open(io.BytesIO(img))
                Img.close()
                text = ocr.run(image)
                content={'result':text, 'img': byteImag ,'imgname': Img.name ,'imgsize': Img.size}
                return render_to_response('ocrresult.html',content)
    else:
        uf = UserForm()
    return render_to_response('ocr.html', {'uf':uf})
class QQGroups(object):
    """QQ Groups Spider"""

    def __init__(self):
        super(QQGroups, self).__init__()
        self.session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Referer': 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=715030901&daid=73&pt_no_auth=1&s_url=http%3A%2F%2Fqqun.qq.com%2Fgroup%2Findex.html%3Fkeyword%3Dtencent',
        }
        self.session.headers.update(headers)
        self.js_ver = '10171'

    def getQRCode(self):
        try:
            url = 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=715030901&daid=73&pt_no_auth=1&s_url=http%3A%2F%2Fqqun.qq.com%2Fgroup%2Findex.html%3Fkeyword%3Dtencent'
            resp=self.session.get(url, timeout=200)
            pattern = r'http://imgcache\.qq\.com/ptlogin/ver/(\d+)/'
            self.js_ver = re.search(pattern, resp.content).group(1)
          
            url = 'http://ptlogin2.qq.com/ptqrshow?appid=715030901&e=2&l=M&s=3&d=72&v=4&t=%.17f&daid=73' % (random())
            resp = self.session.get(url, timeout=200)
        except:
            resp = None
        #print resp
        response=HttpResponse(resp,content_type="image/png")
        response['Cache-Control']= 'no-cache, no-store'
        response['Pragma']= 'no-cache'
        return response
    def qrLogin(self):
        u1 = 'http%3A%2F%2Fqqun.qq.com%2Fgroup%2Findex.html%3Fkeyword%3Dtencent'
        login_sig = self.session.cookies.get_dict().get('pt_login_sig', '')
        url = 'http://ptlogin2.qq.com/ptqrlogin?u1=%s&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-%d&js_ver=%s&js_type=1&login_sig=%s&pt_uistyle=40&aid=715030901&daid=73&' % (
            u1, time() * 1000, self.js_ver, login_sig)
        try:
            errorMsg = ''
            resp = self.session.get(url, timeout=200)
            result = resp.content
            print url
            print result
            if  '二维码未失效' in result:
                status = 0
            elif '二维码认证中' in result:
                status = 1
            elif '登录成功' in result:
                status = 2
            elif '二维码已失效' in result:
                status = 3
            else:
                status = 4
                errorMsg = str(result.text)
        except:
            status = -1
            try:
                errorMsg = resp.status_code
            except:
                pass
        loginResult = {
            'status': status,
            'time': time(),
            'errorMsg': errorMsg,
        }
        resp = json.dumps(loginResult)
        print resp
        response = HttpResponse(resp ,content_type='application/json; charset=UTF-8')
        response['Cache-Control']= 'no-cache; must-revalidate'
        response['Expires']= '-1'
        return response

    def genbkn(self, skey):
        b = 5381
        for i in xrange(0, len(skey)):
            b += (b << 5) + ord(skey[i])
        bkn = (b & 2147483647)
        return str(bkn)

    def qqunSearch(self, request):
        st = request.POST['st']
        pn = int(request.POST['pn'])
        ft = request.POST['ft']
        kw = request.POST['kw'].strip()
        if not kw:
            return render(request, 'qqun.html',
                          { 'error_message': "请输入群关键词",
            })
        skey = self.session.cookies.get_dict().get('skey', '')
        groups = [(u'群名称', u'群号', u'群人数', u'群主', u'群简介')]
        try:
            for page in xrange(0, pn):
                # sort type: 1 deafult, 2 menber, 4 active
                url = 'http://qqun.qq.com/cgi-bin/qun_search/search_group?k=%s&t=&c=1&p=%s&n=8&st=%s&d=1&r=%.17f&bkn=%s&s=3&v=0' % (
                    urllib.quote(kw), page, st, random(), self.genbkn(skey))
                resp = self.session.get(url, timeout=100)
                result = resp.json()
                gList = result.get('gList')
                for item in gList:
                    gName = item['gName'].strip()
                    gc = item['gc']
                    gMemNum = item['gMemNum']
                    gOwner = item['gOwner']
                    gIntro = item['gIntro'].strip()
                    gMeta = (gName, gc, gMemNum, gOwner, gIntro)
                    groups.append(gMeta)
                sleep(2.5)
        except Exception, e:
            # return e
            if len(groups) == 1:
               return render_to_response('qqun.html', { 'error_message': "暂时未找到信息",
            })
        f = BytesIO()
        if ft == 'xls':
            sheet = pe.Sheet(groups)
            f = sheet.save_to_memory('xls', f)
            response = HttpResponse(f,content_type='application/vnd.ms-excel ; charset=UTF-8')
            filename = kw.replace(' ', '_') + '.xls'
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            return response
        elif ft == 'csv':
            #writer = csv.writer(f, dialect='excel', encoding='utf-8')
            response = HttpResponse( content_type='text/csv ; charset=UTF-8')
            writer=csv.writer(response,dialect='excel', encoding='utf-8')
            writer.writerows(groups)
            filename = kw.replace(' ', '_') + '.csv'
            response['Content-Disposition'] = 'attachment; filename="%s"'%filename
            return response

q = QQGroups()
def qqun(request):
    if request.method == 'GET':
        return render_to_response('qqun.html')
    elif request.method == 'POST':
        return q.qqunSearch(request)


def getQRCode(request):
    return q.getQRCode()



def qrLogin(request):
    return q.qrLogin()
def help(request):
    return render_to_response('qqun_man.html')
def generate_qrcode(request):
    img = qrcode.make('http://www.sharejs.com')
    buf = StringIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    return response
