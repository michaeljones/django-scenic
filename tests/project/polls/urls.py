
from django.urls import patterns, re_path


urlpatterns = patterns(
    'polls.views',

    re_path(r'^$', 'index', name='index'),
    re_path(r'^(?P<poll_id>\d+)/$', 'detail', name='detail'),
    re_path(r'^(?P<poll_id>\d+)/results/$', 'results', name='results'),
    re_path(r'^(?P<poll_id>\d+)/vote/$', 'vote', name='vote'),
)
