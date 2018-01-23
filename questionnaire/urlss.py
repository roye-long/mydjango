from django.conf.urls import url
from . import views
app_name = 'questionnaire'
urlpatterns = [
    # ex: /polls/
    url(r'^$',views.index ,name="index"),
    url(r'^questionpage$', views.IndexView.as_view(), name='question'),
    url(r'^(?P<question_id>[0-9]+)/resultlook$', views.resultlook, name='look'),
    # ex: /polls/5/
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^questionpage/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    #url(r'^results/$', views.results, name='result'),
    url(r'^questionpage/(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='result'),
    # ex: /polls/5/vote/
    url(r'^questionpage/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]