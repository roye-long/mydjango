
from django.conf.urls import url
from . import views
app_name = 'weixin'
urlpatterns = [
    # ex: /polls/
    url(r'^$',views.weixin ,name="index"),
]
