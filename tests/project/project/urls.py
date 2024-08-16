
from django.urls import patterns, include, re_path

from django.contrib import admin
admin.autodiscover()

main_patterns = patterns(
    '',
    re_path(r'^$', 'polls.views.main_index', name='index'),
)

urlpatterns = patterns(
    '',

    re_path(r'^$', include((main_patterns, "main", "main"))),

    (r'^admin/', include(admin.site.urls)),

    (r'^polls/', include('polls.urls', namespace='polls')),
)
