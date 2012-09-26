# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from unittest import TestCase

from django.contrib.auth.models import User

from fleetusers.models import (
    UserProfile,
)


class UserProfileTestCase(TestCase):
    """The test suite for the UserProfile model."""

    def test_created_with_user_creation(self):
        user = User.objects.create(username='foo')
        self.assertIsInstance(user.get_profile(), UserProfile)
