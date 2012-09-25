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
        self.user = User.objects.create(username=self.username,
                                        password=self.password)

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'))


class HomeTestCase(BaseViewTestCase):
    """The test suite for the home view."""

    def setUp(self):
        super(BaseViewTestCase, self).setUp()

    def test_home(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Home')
        self.assertTemplateUsed(response, 'index.html')

    def test_upload_new_bill(self):
        pass
