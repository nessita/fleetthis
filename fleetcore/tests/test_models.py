# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from datetime import date, datetime, timedelta
from decimal import Decimal

from django.core.files import File
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from mock import patch

from fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
)
from fleetcore.pdf2cell import (
    EQUIPMENT_PRICE,
    EXCEEDED_MIN,
    EXCEEDED_MIN_PRICE,
    IDL_MIN,
    IDL_PRICE,
    INCLUDED_MIN,
    MONTHLY_PRICE,
    NDL_MIN,
    NDL_PRICE,
    OTHER_PRICE,
    PHONE_NUMBER,
    PLAN,
    REFUNDS,
    SERVICES,
    SMS,
    SMS_PRICE,
    TOTAL_PRICE,
    USER,
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


class BaseModelTestCase(TransactionTestCase):
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

    def assert_no_data_processed(self, pdf_parser_called=False):
        if pdf_parser_called:
            self.mock_pdf_parser.assert_called_with(self.obj.invoice.path)
        else:
            self.assertFalse(self.mock_pdf_parser.called)

        self.assertEqual(Consumption.objects.count(), 0)
        # reload bill from db
        bill = Bill.objects.get(id=self.obj.id)
        self.assertIsNone(bill.billing_date)
        self.assertIsNone(bill.parsing_date)
        self.assertEqual(bill.provider_number, '')

    def test_empty_path(self):
        assert Consumption.objects.count() == 0
        self.obj.invoice = File('')
        self.obj.save()

        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assert_no_data_processed()

    def test_unexistent_path(self):
        assert Consumption.objects.count() == 0
        assert not os.path.exists(self.obj.invoice.path)

        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assert_no_data_processed()

    def test_non_empty_bill_is_parsed(self):
        assert Consumption.objects.count() == 0

        path = os.path.join(TEST_FILES_DIR, 'empty.pdf')
        assert not os.path.exists(path)
        with open(path, 'w') as f:
            self.addCleanup(os.remove, path)

        self.obj.invoice = File(path)
        self.obj.save()

        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assert_no_data_processed()

    def test_missing_phones(self):
        assert Consumption.objects.count() == 0

        path = self.obj.invoice.path
        with open(path, 'w') as f:
            self.addCleanup(os.remove, path)
        assert os.path.exists(self.obj.invoice.path)

        self.mock_pdf_parser.return_value = PDF_PARSED_SAMPLE

        # phones are not previously added, so parse is not successful
        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assert_no_data_processed(pdf_parser_called=True)

    def test_missing_one_phone(self):
        self.test_missing_phones()

        plan = Plan.objects.create(name='PLAN1')
        user = User.objects.create(username='1234567890')
        Phone.objects.create(number='1234567890', plan=plan, user=user)

        # only one phone is in the system, so parse is not successful
        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assert_no_data_processed(pdf_parser_called=True)

    def test_successful_parsing(self):
        self.test_missing_one_phone()
        plan = Plan.objects.create(name='PLAN2')
        user = User.objects.create(username='1987654320')
        Phone.objects.create(number='1987654320', plan=plan, user=user)

        now = datetime.now()
        with patch('fleetcore.models.datetime') as mock_date:
            mock_date.now.return_value = now
            # both phones are in the system, so parse should succeed
            self.obj.parse_invoice()

        self.mock_pdf_parser.assert_called_with(self.obj.invoice.path)
        self.assertEqual(Consumption.objects.count(), 2)

        # reload bill from db
        bill = Bill.objects.get(id=self.obj.id)
        self.assertEqual(bill.billing_date, date(2011, 10, 13))
        self.assertEqual(bill.parsing_date, now)
        self.assertEqual(bill.provider_number, '123456abcd')

        for d in PDF_PARSED_SAMPLE['phone_data']:
            c = Consumption.objects.get(phone__number=d[PHONE_NUMBER])
            self.assertEqual(c.reported_user, d[USER])
            self.assertEqual(c.reported_plan, d[PLAN])
            self.assertEqual(c.monthly_price, d[MONTHLY_PRICE])
            self.assertEqual(c.services, d[SERVICES])
            self.assertEqual(c.refunds, d[REFUNDS])
            self.assertEqual(c.included_min, d[INCLUDED_MIN])
            self.assertEqual(c.exceeded_min, d[EXCEEDED_MIN])
            self.assertEqual(c.exceeded_min_price, d[EXCEEDED_MIN_PRICE])
            self.assertEqual(c.ndl_min, d[NDL_MIN])
            self.assertEqual(c.ndl_min_price, d[NDL_PRICE])
            self.assertEqual(c.idl_min, d[IDL_MIN])
            self.assertEqual(c.idl_min_price, d[IDL_PRICE])
            self.assertEqual(c.sms, d[SMS])
            self.assertEqual(c.sms_price, d[SMS_PRICE])
            self.assertEqual(c.equipment_price, d[EQUIPMENT_PRICE])
            self.assertEqual(c.other_price, d[OTHER_PRICE])
            self.assertEqual(c.reported_total, d[TOTAL_PRICE])
            self.assertEqual(c.bill, self.obj)

    def test_do_not_parse_twice(self):
        self.test_successful_parsing()
        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)


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

    def test_active(self):
        self.assertTrue(self.obj.active)

    def test_inactive(self):
        self.obj.active_to = datetime.now()
        self.obj.save()

        assert self.obj.active_to > self.obj.active_since
        assert datetime.now() > self.obj.active_to

        self.assertFalse(self.obj.active)

    def test_inactive_in_the_future(self):
        self.obj.active_to = datetime.now() + timedelta(days=1)
        self.obj.save()

        assert self.obj.active_to > self.obj.active_since
        assert datetime.now() < self.obj.active_to

        self.assertTrue(self.obj.active)


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
