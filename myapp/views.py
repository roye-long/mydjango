# -*- coding :utf8 -*-
import datetime,json
from django.http import HttpResponse
from django.db.models import  *
from django.shortcuts import render ,render_to_response
from myapp.models import  Jd,Newline
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
    return render_to_response( 'line.html',content)
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

