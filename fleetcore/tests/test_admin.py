# coding: utf-8

from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

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
    def recalculate_url(self):
        return reverse('admin:recalculate', kwargs=dict(bill_id=self.bill.id))

    def test_recalculate(self):
        self.client.get(self.recalculate_url)
        # bill is parsed
        # bill is adjusted
        # response is a redirect to details
