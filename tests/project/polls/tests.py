
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

from .models import Poll


class MainIndexViewTests(TestCase):

    def test_index(self):

        self.client.get(reverse('main:index'))


class IndexViewTests(TestCase):

    def test_index(self):

        self.client.get(reverse('polls:index'))


class DetailViewTests(TestCase):

    def test_detail(self):

        poll = Poll.objects.create(
                pub_date=now()
                )

        self.client.get(reverse('polls:detail', args=[poll.id]))


class ResultsViewTests(TestCase):

    def test_results(self):

        poll = Poll.objects.create(
                pub_date=now()
                )

        self.client.get(reverse('polls:results', args=[poll.id]))

