
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

main_patterns = patterns(
    '',
    url(r'^$', 'polls.views.main_index', name='index'),
)

urlpatterns = patterns(
    '',

    url(r'^$', include((main_patterns, "main", "main"))),

    (r'^admin/', include(admin.site.urls)),

    (r'^polls/', include('polls.urls', namespace='polls')),
)
