
from django.conf.urls import patterns, url


urlpatterns = patterns('polls.views',
    url(r'^$', 'index', name='index'),
    (r'^(?P<poll_id>\d+)/$', 'detail'),
    (r'^(?P<poll_id>\d+)/results/$', 'results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)

