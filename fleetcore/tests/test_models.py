# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from unittest import TestCase

from django.contrib.auth.models import User
from django.core.files import File
from mock import patch

from fleetthis.fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
    UserProfile,
    parse_invoice,
)


class BaseModelTestCase(TestCase):
    """The base test suite for models."""

    model = None
    kwargs = {}

    def setUp(self):
        super(BaseModelTestCase, self).setUp()
        self.obj = None
        if self.model is not None:
            self.obj = self.model.objects.create(**self.kwargs)

    def test_id(self):
        """Model can be created and stored."""
        if self.model is not None:
            self.assertEqual(self.obj.id, 1)
            self.obj.save()


class BillTestCase(TestCase):
    """The test suite for the Bill model."""

    model = Bill


class ConsumptionTestCase(TestCase):
    """The test suite for the Consumption model."""

    model = Consumption


class PhoneTestCase(TestCase):
    """The test suite for the Phone model."""

    model = Phone


class PlanTestCase(TestCase):
    """The test suite for the Plan model."""

    model = Plan


class FleetTestCase(TestCase):
    """The test suite for the Fleet model."""

    model = Fleet


class UserProfileTestCase(TestCase):
    """The test suite for the UserProfile model."""

    model = UserProfile


class ParceInvoiceTestCase(TestCase):
    """The test suite for the parse_invoice method."""

    def setUp(self):
        super(ParceInvoiceTestCase, self).setUp()
        patcher = patch('fleetthis.fleetcore.models.pdf2cell.parse_file')
        self.mock_pdf_parser = patcher.start()
        self.addCleanup(patcher.stop)

        self.owner = User.objects.create(username='owner',
                                         email='owner@example.com')

        self.fleet = Fleet.objects.create(
            owner=self.owner, account_number=123456,
            email='foo@example.com', provider='Fake')

    def test_empty_bill_is_parsed_when_created(self):
        assert Consumption.objects.count() == 0

        self.mock_pdf_parser.return_value = {}
        bill = Bill.objects.create(
            fleet=self.fleet,
            invoice=File(open(__file__), "test_invoice.pdf"))

        self.mock_pdf_parser.assert_called_once_with(bill.invoice.path)
        self.assertEqual(Consumption.objects.count(), 0)
