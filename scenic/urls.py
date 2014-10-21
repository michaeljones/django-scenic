
from django.conf.urls import url

class UrlFactory(object):

    def __init__(self, lookup):
        self.lookup = lookup

    def __call__(self, pattern, name):

        return url(pattern, self.lookup[name], name=name)


