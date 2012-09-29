# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from mock import patch

from fleetcore.admin import (
    BillAdmin,
)


class BillAdminTestCase(TestCase):
    """The test suite for the BillAdmin."""

    def setUp(self):
        super(BillAdminTestCase, self).setUp()
