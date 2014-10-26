
from django.conf.urls import patterns, url


urlpatterns = patterns('polls.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<poll_id>\d+)/$', 'detail', name='detail'),
    url(r'^(?P<poll_id>\d+)/results/$', 'results', name='results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)

