# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch


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
        self.assertContains(response, 'Home')
        self.assertContains(response,
                            '<a href="%s">Logout</a>' % reverse('logout'))
        self.assertTemplateUsed(response, 'index.html')
