
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

from .models import Poll


STATUS_OK = 200
STATUS_REDIRECT = 302

class MainIndexViewTests(TestCase):

    def test_index(self):

        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, STATUS_OK)


class IndexViewTests(TestCase):

    def test_index(self):

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, STATUS_OK)


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

        response = self.client.get(reverse('polls:results', args=[poll.id]))
        self.assertEqual(response.status_code, STATUS_OK)

