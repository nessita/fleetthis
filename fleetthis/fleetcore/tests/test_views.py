# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.models import User
from django.test import TestCase
from mock import patch


class BaseViewTestCase(TestCase):
    """The base test suite for views."""


class HomeTestCase(TestCase):
    """The test suite for the home view."""

    def test_visited(self):
        response = self.client.get('/')
        self.assertContains(response, 'Home')
