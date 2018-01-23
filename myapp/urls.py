from django.conf.urls import url
import views
urlpatterns =[
    url(r'^$',views.sayHello),
    url(r'^lookupline/',views.linelook),
    url(r'^lookupline2/',views.line2look),
    url(r'^ocr/',views.ocr),
    url(r'^qqun/',views.qqun),
    url(r'^qqun_help/',views.help),
    url(r'^getqrcode/',views.getQRCode),
    url(r'^qrlogin/',views.qrLogin)
    #url( r'^static/(?P<path>.*)$', django.views.static.serve,{ 'document_root': settings.STATIC_URL }),
    ]