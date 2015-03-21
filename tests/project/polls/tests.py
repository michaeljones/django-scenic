
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

from .models import Poll, Choice


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

        response = self.client.get(reverse('polls:detail', args=[poll.id]))
        self.assertEqual(response.status_code, STATUS_OK)


class VoteViewTests(TestCase):

    def test_vote(self):

        poll = Poll.objects.create(
            pub_date=now()
        )
        Choice.objects.create(
            poll=poll,
            votes=0
        )

        post_data = {
            'choice': 1
        }

        response = self.client.post(reverse('polls:vote', args=[poll.id]), post_data)
        self.assertEqual(response.status_code, STATUS_REDIRECT)

    def test_invalid_vote(self):

        poll = Poll.objects.create(
            pub_date=now()
        )

        post_data = {
            'choice': 100
        }

        response = self.client.post(reverse('polls:vote', args=[poll.id]), post_data)
        self.assertEqual(response.status_code, STATUS_OK)


class ResultsViewTests(TestCase):

    def test_results(self):

        poll = Poll.objects.create(
            pub_date=now()
        )

        response = self.client.get(reverse('polls:results', args=[poll.id]))
        self.assertEqual(response.status_code, STATUS_OK)
