# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch

import fleetcore
from fleetcore.tests.factory import Factory


class BaseViewTestCase(TestCase):
    """The base test suite for views."""

    username = 'foo'
    password = 'bar'

    def setUp(self):
        super(BaseViewTestCase, self).setUp()
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)


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
        self.factory = Factory()
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
        consumption = self.factory.make_consumption(user=self.user)
        bill = consumption.bill
        bill.billing_date = date.today()
        bill.save()

        # more than a year before
        another_consumption = self.factory.make_consumption()
        bill = another_consumption.bill
        bill.billing_date = date.today() - timedelta(days=400)
        bill.save()

        response = self.client.get(reverse('home'))
        self.assertIn('consumptions', response.context)
        consumptions = response.context['consumptions']
        self.assertEqual(consumptions.count(), 1)
        self.assertEqual(consumptions[0], consumption)


class UpdateTestCase(TestCase):
    """Test suite for do_update view."""

    def setUp(self):
        self.url = reverse('updated-source-hook')

    def test_do_update_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    @patch('fleetthis.views.call_command')
    def test_do_update_post(self, mock_call_command):
        response = self.client.post(self.url)
        mock_call_command.assert_called_with('deploy')
        self.assertEqual(response.status_code, 200)
