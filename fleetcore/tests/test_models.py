# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import itertools
import logging
import os

from copy import deepcopy
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.core.files import File
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from mock import call, patch

from fleetcore.models import (
    Bill,
    Consumption,
    DataPack,
    Fleet,
    Penalty,
    Phone,
    Plan,
    SMSPack,
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
    'bill_debt': Decimal('123.45'),
    'bill_number': '123456abcd',
    'bill_total': Decimal('1234.56'),
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

        patcher = patch('fleetcore.models.logging')
        self.mock_logging = patcher.start()
        self.addCleanup(self.mock_logging.stop)

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

    def _make_phone(self, plan, number):
        plan = Plan.objects.create(name=plan)
        user = User.objects.create(username=number)
        return Phone.objects.create(number=number, current_plan=plan,
                                    user=user)

    def assert_no_data_processed(self, pdf_parser_called=False):
        if pdf_parser_called:
            self.mock_pdf_parser.assert_called_with(self.obj.invoice.path,
                                                    format='new')
        else:
            self.assertFalse(self.mock_pdf_parser.called)

        self.assertEqual(Consumption.objects.count(), 0)
        # reload bill from db
        bill = Bill.objects.get(id=self.obj.id)
        self.assertIsNone(bill.billing_date)
        self.assertIsNone(bill.parsing_date)
        self.assertEqual(bill.provider_number, '')
        self.assertEqual(bill.billing_debt, Decimal('0'))
        self.assertEqual(bill.billing_total, Decimal('0'))

    def assert_consumption_processed(self, data, bill=None, real_plan=None):
        if bill is None:
            bill = self.obj
        if real_plan is None:
            real_plan = Plan.objects.get(name=data[PLAN])

        c = Consumption.objects.get(bill=bill,
                                    phone__number=data[PHONE_NUMBER])
        self.assertEqual(c.bill, bill)
        self.assertEqual(c.phone.number, data[PHONE_NUMBER])
        self.assertEqual(c.plan, real_plan)
        self.assertEqual(c.reported_user, data[USER])
        self.assertEqual(c.reported_plan, data[PLAN])
        self.assertEqual(c.monthly_price, data[MONTHLY_PRICE])
        self.assertEqual(c.services, data[SERVICES])
        self.assertEqual(c.refunds, data[REFUNDS])
        self.assertEqual(c.included_min, data[INCLUDED_MIN])
        self.assertEqual(c.exceeded_min, data[EXCEEDED_MIN])
        self.assertEqual(c.exceeded_min_price, data[EXCEEDED_MIN_PRICE])
        self.assertEqual(c.ndl_min, data[NDL_MIN])
        self.assertEqual(c.ndl_min_price, data[NDL_PRICE])
        self.assertEqual(c.idl_min, data[IDL_MIN])
        self.assertEqual(c.idl_min_price, data[IDL_PRICE])
        self.assertEqual(c.sms, data[SMS])
        self.assertEqual(c.sms_price, data[SMS_PRICE])
        self.assertEqual(c.equipment_price, data[EQUIPMENT_PRICE])
        self.assertEqual(c.other_price, data[OTHER_PRICE])
        self.assertEqual(c.reported_total, data[TOTAL_PRICE])

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
        self._make_phone(plan='PLAN1', number='1234567890')

        # only one phone is in the system, so parse is not successful
        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)
        self.assert_no_data_processed(pdf_parser_called=True)

    def test_successful_parsing(self):
        self.test_missing_one_phone()
        self._make_phone(plan='PLAN2', number='1987654320')

        now = datetime.now()
        with patch('fleetcore.models.datetime') as mock_date:
            mock_date.now.return_value = now
            # both phones are in the system, so parse should succeed
            self.obj.parse_invoice()

        self.mock_pdf_parser.assert_called_with(self.obj.invoice.path,
                                                format='new')
        self.assertEqual(Consumption.objects.count(), 2)

        # reload bill from db
        bill = Bill.objects.get(id=self.obj.id)
        self.assertEqual(bill.billing_date, date(2011, 10, 13))
        self.assertEqual(bill.billing_total, Decimal('1234.56'))
        self.assertEqual(bill.billing_debt, Decimal('123.45'))
        self.assertEqual(bill.parsing_date, now)
        self.assertEqual(bill.provider_number, '123456abcd')

        for d in PDF_PARSED_SAMPLE['phone_data']:
            self.assert_consumption_processed(data=d)

    def test_do_not_parse_twice(self):
        self.test_successful_parsing()
        self.assertRaises(Bill.ParseError, self.obj.parse_invoice)


class CalculatePenaltiesTestCase(BillTestCase):
    """The test suite for the calculate_penalties method for the Bill model."""

    def setUp(self):
        super(CalculatePenaltiesTestCase, self).setUp()

        data = (
            1234567890,
            1234560987,
            1265437890,
        )
        self.plan1 = Plan.objects.create(name='PLAN1', included_min=100)
        for p in data:
            self._make_consumption(self.plan1, p)

        with open(self.obj.invoice.path, 'w') as f:
            self.addCleanup(os.remove, self.obj.invoice.path)
        self.mock_pdf_parser.return_value = {}
        self.obj.parse_invoice()
        assert self.obj.parsing_date is not None

    def _make_consumption(self, plan, phone_number, bill=None):
        phone = Phone.objects.create(
            number=phone_number, current_plan=plan,
            user=User.objects.create(username=str(phone_number)),
        )
        if bill is None:
            bill = self.obj
        return Consumption.objects.create(phone=phone, bill=bill, plan=plan)

    def assert_no_penalties(self):
        self.assertEqual(Penalty.objects.filter(bill=self.obj).count(), 0)
        for c in Consumption.objects.all():
            self.assertEqual(c.penalty_min, 0)
            self.assertEqual(c.penalty_sms, 0)

    def test_no_parsing_date(self):
        self.obj.parsing_date = None
        self.obj.save()

        self.assertRaises(Bill.AdjustmentError, self.obj.calculate_penalties)
        self.assert_no_penalties()

    def test_parsed_but_no_data(self):
        Consumption.objects.all().delete()

        self.obj.calculate_penalties()

        self.assert_no_penalties()

    def test_with_data_no_min_clearing_less_minutes(self):
        self.plan1.with_min_clearing = False
        self.plan1.included_min = 100
        self.plan1.save()

        for c in Consumption.objects.filter(plan=self.plan1):
            c.included_min = 80
            c.save()

        self.obj.calculate_penalties()

        self.assert_no_penalties()

        for c in Consumption.objects.all():
            self.assertEqual(c.penalty_min, 0)
            self.assertEqual(c.penalty_sms, 0)

    def test_with_data_no_min_clearing_more_minutes(self):
        self.plan1.with_min_clearing = False
        self.plan1.included_min = 100
        self.plan1.save()

        for c in Consumption.objects.filter(plan=self.plan1):
            c.included_min = 100
            c.exceeded_min = 20
            c.save()

        self.obj.calculate_penalties()

        self.assert_no_penalties()

        for c in Consumption.objects.all():
            self.assertEqual(c.penalty_min, 0)
            self.assertEqual(c.penalty_sms, 0)

    def test_with_data_with_min_clearing_all_minutes_used(self):
        assert self.plan1.with_min_clearing
        self.plan1.included_min = 100
        self.plan1.save()

        for c in Consumption.objects.filter(plan=self.plan1):
            c.included_min = 100
            c.save()

        self.obj.calculate_penalties()
        self.assert_no_penalties()

    def test_with_data_with_min_clearing_minutes_left(self):
        self.plan1.with_min_clearing = True
        self.plan1.included_min = 100
        self.plan1.save()

        c1, c2, c3 = Consumption.objects.filter(plan=self.plan1)

        c1.included_min = 35
        c1.exceeded_min = 15
        c1.save()

        c2.included_min = 80
        c2.save()

        c3.included_min = 110
        c3.exceeded_min = 10
        c3.save()

        # total available minutes is 300, only 250 were used.
        # penalty is 50 minutes to be distributed between c1 and c2

        self.obj.calculate_penalties()

        self.assertEqual(Penalty.objects.filter(bill=self.obj).count(), 1)
        penalty = Penalty.objects.get()
        self.assertEqual(penalty.bill, self.obj)
        self.assertEqual(penalty.plan, self.plan1)
        self.assertEqual(penalty.minutes, 50)
        self.assertEqual(penalty.sms, 0)

    def test_with_more_plans(self):
        self.test_with_data_with_min_clearing_minutes_left()

        plan2 = Plan.objects.create(name='PLAN2', included_min=333)
        c = self._make_consumption(plan2, 1987654320)
        c.included_min = 20
        c.exceeded_min = 13
        c.save()

        self.obj.calculate_penalties()
        self.mock_logging.warning.assert_called_once_with(
            'Penalty for "%s" and "%s" already exists, deleting.',
            self.obj, self.plan1)

        # two penalties, one from the invoked test for PLAN1
        # and another from this one for PLAN2
        self.assertEqual(Penalty.objects.filter(bill=self.obj).count(), 2)
        # penalty for PLAN1 was already tested, but let's test it again
        # because it was deleted and re-added
        penalty = Penalty.objects.get(plan=self.plan1)
        self.assertEqual(penalty.bill, self.obj)
        self.assertEqual(penalty.minutes, 50)
        self.assertEqual(penalty.sms, 0)
        # assert over the newly created penalty for PLAN2
        penalty = Penalty.objects.get(plan=plan2)
        self.assertEqual(penalty.bill, self.obj)
        self.assertEqual(penalty.minutes, 300)
        self.assertEqual(penalty.sms, 0)

    def test_with_other_bills(self):
        bill = self.factory.make_bill()
        plan2 = Plan.objects.create(name='PLAN2', included_min=333)
        self._make_consumption(plan2, 7539518520, bill=bill)
        self._make_consumption(plan2, 7539518521, bill=bill)
        assert plan2.with_min_clearing

        self.plan1.included_min = 0  # do not have spare minutes
        self.plan1.save()

        self.obj.calculate_penalties()

        self.assert_no_penalties()

    def test_penalties_applied(self):
        self.test_with_data_with_min_clearing_minutes_left()
        c1, c2, c3 = Consumption.objects.filter(plan=self.plan1)
        # c1 has 50 used mins, and c2 has 80
        # penalty to apply is 50 minutes, so c1 should end up with
        # 40 penalty mins, and c2 with 10 (thus both will have a total
        # of 90 used mins).

        self.assertEqual(c1.penalty_min, 40)
        self.assertEqual(c1.penalty_sms, 0)

        self.assertEqual(c2.penalty_min, 10)
        self.assertEqual(c2.penalty_sms, 0)

        self.assertEqual(c3.penalty_min, 0)
        self.assertEqual(c3.penalty_sms, 0)


class ConsumptionTestCase(BaseModelTestCase):
    """The test suite for the Consumption model."""

    model = Consumption

    def test_mins(self):
        self.assertEqual(self.obj.mins, 0)

    def test_mins_is_set_on_save(self):
        for i, j, k in itertools.product([0, 13], repeat=3):
            self.obj.included_min = i
            self.obj.exceeded_min = j
            self.obj.penalty_min = k

            self.obj.save()
            self.assertEqual(self.obj.mins, i + j)

    def test_wrong_mins_is_corrected_on_save(self):
        for i, j, k in itertools.product([0, 19], repeat=3):
            self.obj.included_min = i
            self.obj.exceeded_min = j
            self.obj.penalty_min = k
            self.obj.mins = (i + j) / 2

            self.obj.save()
            self.assertEqual(self.obj.mins, i + j)

    def test_total_min(self):
        self.assertEqual(self.obj.total_min, 0)

    def test_total_min_is_set_on_save(self):
        for i, j, k in itertools.product([0, 13], repeat=3):
            self.obj.included_min = i
            self.obj.exceeded_min = j
            self.obj.penalty_min = k

            self.obj.save()
            self.assertEqual(self.obj.total_min, i + j + k)

    def test_wrong_total_min_is_corrected_on_save(self):
        for i, j, k in itertools.product([0, 19], repeat=3):
            self.obj.included_min = i
            self.obj.exceeded_min = j
            self.obj.penalty_min = k
            self.obj.total_min = (i + j + k) / 2

            self.obj.save()
            self.assertEqual(self.obj.total_min, i + j + k)

    def test_total_sms(self):
        self.assertEqual(self.obj.total_sms, 0)

    def test_total_sms_is_set_on_save(self):
        for i, k in itertools.product([0, 13], repeat=2):
            self.obj.sms = i
            self.obj.penalty_sms = k

            self.obj.save()
            self.assertEqual(self.obj.total_sms, i + k)

    def test_wrong_total_sms_is_corrected_on_save(self):
        for i, k in itertools.product([0, 19], repeat=2):
            self.obj.sms = i
            self.obj.penalty_sms = k
            self.obj.total_sms = (i + k) / 2

            self.obj.save()
            self.assertEqual(self.obj.total_sms, i + k)


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


class DataPackTestCase(BaseModelTestCase):
    """The test suite for the DataPack model."""

    model = DataPack


class SMSPackTestCase(BaseModelTestCase):
    """The test suite for the SMSPack model."""

    model = SMSPack


class FleetTestCase(BaseModelTestCase):
    """The test suite for the Fleet model."""

    model = Fleet


class PenaltyTestCase(BaseModelTestCase):
    """The test suite for the Penalty model."""

    model = Penalty
