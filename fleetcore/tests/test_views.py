# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch

import fleetcore


class BaseViewTestCase(TestCase):
    """The base test suite for views."""

    username = 'foo'
    password = 'bar'

    def setUp(self):
        super(BaseViewTestCase, self).setUp()
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)

    def test_home(self):
        response = self.client.get(reverse('home'))
        expected = reverse('login') + '?next=' + reverse('home')
        self.assertRedirects(response, expected)


class AuthenticatedTestCase(BaseViewTestCase):
    """The test suite for the home view."""

    def setUp(self):
        super(AuthenticatedTestCase, self).setUp()
        self.client.login(username=self.username, password=self.password)

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response,
                            '<a href="%s">Logout</a>' % reverse('logout'))
        self.assertTemplateUsed(response, 'index.html')

    def test_link_to_admin_if_not_superuser(self):
        assert not self.user.is_superuser

        response = self.client.get(reverse('home'))
        self.assertNotContains(response, reverse('admin:index'))

    def test_link_to_admin_if_superuser(self):
        self.user.is_superuser = True
        self.user.save()

        response = self.client.get(reverse('home'))
        self.assertContains(response, reverse('admin:index'))
