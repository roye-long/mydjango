from django.conf.urls import url
import views
urlpatterns =[
    url(r'^$',views.sayHello),
    url(r'^lookupline/',views.linelook),
    url(r'^lookupline2/',views.line2look)
    #url( r'^static/(?P<path>.*)$', django.views.static.serve,{ 'document_root': settings.STATIC_URL }),
    ]