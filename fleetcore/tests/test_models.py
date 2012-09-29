# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from datetime import datetime
from decimal import Decimal

from django.core.files import File
from django.contrib.auth.models import User
from django.test import TestCase
from mock import patch

from fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
)

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')
PDF_PARSED_SAMPLE = {
    'bill_date': datetime(2011, 10, 13),
    'bill_number': '123456abcd',
    'phone_data': [
        [1234567890, 'Foo, Bar', 'PLAN1',
         Decimal('35.0'), Decimal('45.0'), Decimal('0.0'),
         Decimal('103.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('45.0'), Decimal('10.80'),
         Decimal('0.0'), Decimal('0.0'), Decimal('90.80')],
        [1987654320, 'Skywalker, Luke', 'PLAN2',
         Decimal('35.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('190.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('19.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('35.0')],
    ],
}


class BaseModelTestCase(TestCase):
    """The base test suite for models."""

    model = None
    kwargs = {}

    def setUp(self):
        super(BaseModelTestCase, self).setUp()
        self.obj = None
        if self.model is not None:
            self.obj = self.model.objects.create(**self.kwargs)
            self.addCleanup(self.obj.delete)

    def test_id(self):
        """Model can be created and stored."""
        if self.model is not None:
            self.assertEqual(self.obj.id, 1)
            self.obj.save()


class BillTestCase(BaseModelTestCase):
    """The test suite for the Bill model."""

    model = Bill

    def setUp(self):
        user = User.objects.create_user(username='fleet-owner')
        self.addCleanup(user.delete)
        fleet = Fleet.objects.create(owner=user, account_number=24680)
        self.addCleanup(fleet.delete)
        self.kwargs = dict(fleet=fleet, invoice='zaraza.pdf')
        super(BillTestCase, self).setUp()

        patcher = patch('fleetcore.models.pdf2cell.parse_file')
        self.mock_pdf_parser = patcher.start()
        self.addCleanup(patcher.stop)

    def test_empty_path(self):
        assert Consumption.objects.count() == 0
        self.obj.invoice = File('')
        self.obj.save()

        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assertFalse(self.mock_pdf_parser.called)
        self.assertEqual(Consumption.objects.count(), 0)

    def test_unexistent_path(self):
        assert Consumption.objects.count() == 0
        assert not os.path.exists(self.obj.invoice.path)

        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assertFalse(self.mock_pdf_parser.called)
        self.assertEqual(Consumption.objects.count(), 0)

    def test_non_empty_bill_is_parsed(self):
        assert Consumption.objects.count() == 0

        path = os.path.join(TEST_FILES_DIR, 'empty.pdf')
        assert not os.path.exists(path)
        with open(path, 'w') as f:
            self.addCleanup(os.remove, path)

        self.obj.invoice = File(path)
        self.obj.save()

        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assertFalse(self.mock_pdf_parser.called)
        self.assertEqual(Consumption.objects.count(), 0)

    def test_missing_phones(self):
        assert Consumption.objects.count() == 0

        path = self.obj.invoice.path
        with open(path, 'w') as f:
            self.addCleanup(os.remove, path)
        assert os.path.exists(self.obj.invoice.path)

        self.mock_pdf_parser.return_value = PDF_PARSED_SAMPLE

        # phones are not previously added, so parse is not successful
        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.mock_pdf_parser.assert_called_once_with(self.obj.invoice.path)
        self.assertEqual(Consumption.objects.count(), 0)

    def test_missing_one_phone(self):
        self.test_missing_phones()

        plan = Plan.objects.create(name='PLAN1')
        user = User.objects.create(username='1234567890')
        Phone.objects.create(number='1234567890', plan=plan, user=user)

        # only one phone is in the system, so parse is not successful
        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.mock_pdf_parser.assert_called_with(self.obj.invoice.path)
        self.assertEqual(Consumption.objects.count(), 0)

    def test_no_phone_missing(self):
        self.test_missing_one_phone()
        plan = Plan.objects.create(name='PLAN2')
        user = User.objects.create(username='1987654320')
        Phone.objects.create(number='1987654320', plan=plan, user=user)

        # both phones are in the system, so parse should succeed
        self.obj.parse_invoice()

        self.mock_pdf_parser.assert_called_with(self.obj.invoice.path)
        self.assertEqual(Consumption.objects.count(), 2)


class ConsumptionTestCase(BaseModelTestCase):
    """The test suite for the Consumption model."""

    model = Consumption

    def setUp(self):
        user = User.objects.create_user(username='fleet-owner')
        self.addCleanup(user.delete)
        fleet = Fleet.objects.create(owner=user, account_number=24680)
        self.addCleanup(fleet.delete)
        bill = Bill.objects.create(fleet=fleet, invoice='yadda.pdf')
        self.addCleanup(bill.delete)

        user = User.objects.create_user(username='phone-user')
        self.addCleanup(user.delete)
        plan = Plan.objects.create()
        self.addCleanup(plan.delete)
        phone = Phone.objects.create(number=1234567890, user=user, plan=plan)
        self.addCleanup(phone.delete)
        self.kwargs = dict(bill=bill, phone=phone)
        super(ConsumptionTestCase, self).setUp()


class PhoneTestCase(BaseModelTestCase):
    """The test suite for the Phone model."""

    model = Phone

    def setUp(self):
        user = User.objects.create_user(username='test')
        self.addCleanup(user.delete)
        plan = Plan.objects.create(included_minutes=123, included_sms=321)
        self.addCleanup(plan.delete)
        self.kwargs = dict(number=1234567890, user=user, plan=plan)
        super(PhoneTestCase, self).setUp()


class PlanTestCase(BaseModelTestCase):
    """The test suite for the Plan model."""

    model = Plan
    kwargs = dict(included_minutes=123, included_sms=321)


class FleetTestCase(BaseModelTestCase):
    """The test suite for the Fleet model."""

    model = Fleet

    def setUp(self):
        user = User.objects.create_user(username='fleet-owner')
        self.addCleanup(user.delete)
        self.kwargs = dict(owner=user, account_number=24680)
        super(FleetTestCase, self).setUp()
