
from django.urls import re_path


class RePathFactory(object):

    def __init__(self, lookup):
        self.lookup = lookup

    def __call__(self, pattern, name):

        return re_path(pattern, self.lookup[name], name=name)
