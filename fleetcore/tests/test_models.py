# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from unittest import TestCase

from django.contrib.auth.models import User
from mock import patch

from fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
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
