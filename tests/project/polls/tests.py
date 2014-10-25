
from django.core.urlresolvers import reverse
from django.test import TestCase


class MainIndexViewTests(TestCase):

    def test_index(self):

        self.client.get(reverse('main:index'))


class IndexViewTests(TestCase):

    def test_index(self):

        self.client.get(reverse('polls:index'))

