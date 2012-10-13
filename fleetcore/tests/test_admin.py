# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import Mock, patch

from fleetcore.admin import (
    BillAdmin,
)
from fleetcore.models import (
    Bill,
)
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

        patcher = patch.object(self.bill, 'make_adjustments')
        self.make_adjustments_mock = patcher.start()
        self.addCleanup(patcher.stop)

        self.admin_user = self.factory.make_admin_user(password='admin')
        self.client.login(username=self.admin_user.username,
                          password='admin')

    @property
    def process_invoice_url(self):
        return reverse('admin:process-invoice',
                       kwargs=dict(bill_id=self.bill.id))

    def test_process_invoice(self):
        response = self.client.get(self.process_invoice_url)
        # bill is parsed
        # bill is adjusted
        # response is a redirect to details

    def test_process_invoice_with_bill_parsed(self):
        self.bill.parse_invoice()
        response = self.client.get(self.process_invoice_url)
        # not error
        # bill is adjusted
        # response is a redirect to details

    def test_process_invoice_with_parse_error(self):
        self.bill.parse_invoice = Mock()
        self.bill.parse_invoice.side_effect = Bill.ParseError('foo')
        response = self.client.get(self.process_invoice_url)
        # response is a redirect to '..' with error message 'foo'

    def test_process_invoice_with_adjustment_error(self):
        self.bill.make_adjustments = Mock()
        self.bill.make_adjustments.side_effect = Bill.AdjustmentError('foo')
        response = self.client.get(self.process_invoice_url)
        # response is a redirect to '..' with error message 'foo'
