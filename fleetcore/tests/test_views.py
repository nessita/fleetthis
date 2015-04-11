# coding: utf-8

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from fleetcore.tests.factory import Factory


User = get_user_model()


class BaseViewTestCase(TestCase):
    """The base test suite for views."""

    username = 'foo'
    password = 'bar'

    def setUp(self):
        super(BaseViewTestCase, self).setUp()
        self.factory = Factory()
        self._create_test_data()

    def _create_test_data(self):
        self.leader = User.objects.create_user(
            username='leader', password='leader')
        self.user = User.objects.create_user(
            username=self.username, password=self.password, leader=self.leader)

        self.consumption = self.factory.make_consumption(user=self.user)
        bill = self.consumption.bill
        bill.billing_date = date.today()
        bill.save()

        # more than a year before
        self.old_consumption = self.factory.make_consumption(user=self.user)
        bill = self.old_consumption.bill
        bill.billing_date = date.today() - timedelta(days=400)
        bill.save()


class AnonymousTestCase(BaseViewTestCase):
    """The test suite for the home view as anonymous user."""

    def test_home(self):
        response = self.client.get(reverse('home'))
        expected = reverse('login') + '?next=' + reverse('home')
        self.assertRedirects(response, expected)


class AuthenticatedHomePageTestCase(BaseViewTestCase):
    """The test suite for the home view as authenticated user."""

    def setUp(self):
        super(AuthenticatedHomePageTestCase, self).setUp()
        self.client.login(username=self.username, password=self.password)

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response,
                            '<a href="%s">Logout</a>' % reverse('logout'))
        self.assertTemplateUsed(response, 'fleetcore/index.html')

    def test_link_to_admin_if_not_superuser(self):
        assert not self.user.is_superuser

        response = self.client.get(reverse('home'))
        self.assertNotContains(response, reverse('admin:index'))

    def test_link_to_admin_if_superuser(self):
        self.user.is_superuser = True
        self.user.save()

        response = self.client.get(reverse('home'))
        self.assertContains(response, reverse('admin:index'))

    def test_homepage_recent_consumptions(self):
        response = self.client.get(reverse('home'))
        self.assertIn('consumptions', response.context)
        consumptions = response.context['consumptions']
        self.assertEqual(consumptions.count(), 1)
        self.assertEqual(consumptions[0], self.consumption)


class UserDetailsTestCase(BaseViewTestCase):

    def test_login_required(self):
        url = reverse('user-details', args=['foo'])
        response = self.client.get(url)
        expected = reverse('login') + '?next=' + url
        self.assertRedirects(response, expected)

    def test_leadership_required(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('user-details', args=['foo'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_leader_get_access(self):
        self.client.login(username='leader', password='leader')
        url = reverse('user-details', args=['foo'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_user'], self.user)
        self.assertEqual(response.context['consumptions'].count(), 1)


class ConsumptionHistoryTestCase(BaseViewTestCase):

    def test_login_required(self):
        url = reverse('consumption-history')
        response = self.client.get(url)
        expected = reverse('login') + '?next=' + url
        self.assertRedirects(response, expected)

    def test_logged_in_user_history(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('consumption-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_user'], self.user)
        self.assertEqual(response.context['consumptions'].count(), 2)

    def test_leadership_required(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('user-consumption-history', args=['foo'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_leader_get_access(self):
        self.client.login(username='leader', password='leader')
        url = reverse('user-consumption-history', args=['foo'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_user'], self.user)
        self.assertEqual(response.context['consumptions'].count(), 2)
