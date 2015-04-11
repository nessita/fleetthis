# coding: utf-8

from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import Mock, patch

from fleetcore.models import Bill
from fleetcore.tests.factory import Factory


class BillAdminTestCase(TestCase):
    """The test suite for the BillAdmin."""

    def setUp(self):
        super(BillAdminTestCase, self).setUp()
        self.factory = Factory()
        self.bill = self.factory.make_bill()

        patcher = patch.object(self.bill, 'parse_invoice')
        self.parse_invoice_mock = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch.object(self.bill, 'calculate_penalties')
        self.calculate_penalties_mock = patcher.start()
        self.addCleanup(patcher.stop)

        self.admin_user = self.factory.make_admin_user(password='admin')
        self.client.login(username=self.admin_user.username,
                          password='admin')

    @property
    def process_invoice_url(self):
        return reverse('admin:process-invoice',
                       kwargs=dict(bill_id=self.bill.id))

    def test_process_invoice(self):
        self.client.get(self.process_invoice_url)
        # bill is parsed
        # bill is adjusted
        # response is a redirect to details

    def test_process_invoice_with_bill_parsed(self):
        self.bill.parse_invoice()
        self.client.get(self.process_invoice_url)
        # not error
        # bill is adjusted
        # response is a redirect to details

    def test_process_invoice_with_parse_error(self):
        self.bill.parse_invoice = Mock()
        self.bill.parse_invoice.side_effect = Bill.ParseError('foo')
        self.client.get(self.process_invoice_url)
        # response is a redirect to '..' with error message 'foo'

    def test_process_invoice_with_adjustment_error(self):
        self.bill.calculate_penalties = Mock()
        self.bill.calculate_penalties.side_effect = Bill.AdjustmentError('foo')
        self.client.get(self.process_invoice_url)
        # response is a redirect to '..' with error message 'foo'
