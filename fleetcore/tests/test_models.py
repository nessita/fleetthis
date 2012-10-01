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
from fleetcore.tests.factory import Factory

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')
PDF_PARSED_SAMPLE = {
    'bill_date': datetime(2011, 10, 13),
    'bill_number': '123456abcd',
    'phone_data': [
        # PHONE_NUMBER, USER, PLAN,
        [1234567890, 'Foo, Bar', 'PLAN1',
         # MONTHLY_PRICE, SERVICES, REFUNDS,
         Decimal('35.0'), Decimal('45.0'), Decimal('0.0'),
         # INCLUDED_MIN, EXCEEDED_MIN, EXCEEDED_MIN_PRICE,
         Decimal('103.0'), Decimal('0.0'), Decimal('0.0'),
         # NDL_MIN, NDL_PRICE, IDL_MIN,
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         # IDL_PRICE, SMS, SMS_PRICE,
         Decimal('0.0'), Decimal('45.0'), Decimal('10.80'),
         # EQUIPMENT_PRICE, OTHER_PRICE, TOTAL_PRICE
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
        self.factory = Factory()
        self.obj = None
        if self.model is not None:
            maker = getattr(self.factory,
                            'make_%s' % self.model.__name__.lower())
            self.obj = maker(**self.kwargs)

    def test_id(self):
        """Model can be created and stored."""
        if self.model is not None:
            self.assertEqual(self.obj.id, 1)
            self.obj.save()


class BillTestCase(BaseModelTestCase):
    """The test suite for the Bill model."""

    model = Bill

    def setUp(self):
        super(BillTestCase, self).setUp()

        patcher = patch('fleetcore.models.pdf2cell.parse_file')
        self.mock_pdf_parser = patcher.start()
        self.addCleanup(patcher.stop)


class ParseInvoiceTestCase(BillTestCase):
    """The test suite for the parse_invoice method for the Bill model."""

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


class MakeAdjustmentsTestCase(BillTestCase):
    """The test suite for the make_adjustments method for the Bill model."""

    def setUp(self):
        super(MakeAdjustmentsTestCase, self).setUp()

        data = (
            ('PLAN1', 1234567890),
            ('PLAN1', 1234560987),
            ('PLAN1', 1265437890),
            ('PLAN2', 1987654320),
        )
        for p, i in data:
            plan, created = Plan.objects.get_or_create(name=p)
            if created:
                setattr(self, p.lower(), plan)

            phone = Phone.objects.create(
                number=i, plan=plan,
                user=User.objects.create(username=str(i)),
            )
            Consumption.objects.create(
                phone=phone, bill=self.obj,
            )

        with open(self.obj.invoice.path, 'w') as f:
            self.addCleanup(os.remove, self.obj.invoice.path)
        self.mock_pdf_parser.return_value = {}
        self.obj.parse_invoice()
        assert self.obj.parsing_date is not None

    def test_no_parsing_date(self):
        self.obj.parsing_date = None
        self.obj.save()

        self.assertRaises(Bill.AdjustmentError, self.obj.make_adjustments)
        self.assertEqual(self.obj.min_penalty, 0)
        self.assertEqual(self.obj.sms_penalty, 0)

    def test_parsed_but_no_data(self):
        self.obj.make_adjustments()
        self.assertEqual(self.obj.min_penalty, 0)
        self.assertEqual(self.obj.sms_penalty, 0)

    def test_parsed_with_data_no_min_clearing_less_minutes(self):
        self.plan1.with_min_clearing = False
        self.plan1.included_minutes = 100
        self.plan1.save()

        for c in Consumption.objects.filter(phone__plan=self.plan1):
            c.included_min = 80
            c.save()

        self.obj.make_adjustments()

        self.assertEqual(self.obj.min_penalty, 0)
        self.assertEqual(self.obj.sms_penalty, 0)

        for c in Consumption.objects.all():
            self.assertEqual(c.min_penalty, 0)
            self.assertEqual(c.sms_penalty, 0)

    def test_parsed_with_data_no_min_clearing_more_minutes(self):
        self.plan1.with_min_clearing = False
        self.plan1.included_minutes = 100
        self.plan1.save()

        for c in Consumption.objects.filter(phone__plan=self.plan1):
            c.included_min = 100
            c.exceeded_min = 20
            c.save()

        self.obj.make_adjustments()

        self.assertEqual(self.obj.min_penalty, 0)
        self.assertEqual(self.obj.sms_penalty, 0)

        for c in Consumption.objects.all():
            self.assertEqual(c.min_penalty, 0)
            self.assertEqual(c.sms_penalty, 0)

    def test_parsed_with_data_with_min_clearing_all_minutes_used(self):
        assert self.plan1.with_min_clearing
        self.plan1.included_minutes = 100
        self.plan1.save()

        for c in Consumption.objects.filter(phone__plan=self.plan1):
            c.included_min = 100
            c.save()

        self.obj.make_adjustments()

    def test_parsed_with_data_with_min_clearing_minutes_left(self):
        self.plan1.with_min_clearing = False
        self.plan1.included_minutes = 100
        self.plan1.save()

        c1, c2, c3 = Consumption.objects.filter(phone__plan=self.plan1)

        c1.included_min = 50
        c1.save()

        c2.included_min = 80
        c2.save()

        c3.included_min = 120
        c3.save()

        # total available minutes is 300, only 250 were used.
        # penalty is 50 minutes to be distributed between c1 and c2

        self.obj.make_adjustments()

        self.assertEqual(self.obj.min_penalty, 50)
        self.assertEqual(self.obj.sms_penalty, 0)

        for c in Consumption.objects.all():
            self.assertEqual(c.min_penalty, 0)
            self.assertEqual(c.sms_penalty, 0)


class ConsumptionTestCase(BaseModelTestCase):
    """The test suite for the Consumption model."""

    model = Consumption


class PhoneTestCase(BaseModelTestCase):
    """The test suite for the Phone model."""

    model = Phone

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


class FleetTestCase(BaseModelTestCase):
    """The test suite for the Fleet model."""

    model = Fleet
