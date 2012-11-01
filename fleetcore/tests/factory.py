# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import random
import string

from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import partial

from django.contrib.auth.models import User

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


class Factory(object):
    """A factory of models."""

    def make_random_string(self, length=10):
        return ''.join(random.choice(string.letters + string.digits)
                       for i in xrange(length))

    def make_random_number(self, digits=10):
        return int(random.random() * (10 ** digits))

    def make_user(self, **kwargs):
        _kwargs = dict(username='username-%s' % self.make_random_number())
        _kwargs.update(kwargs)
        result = User.objects.create_user(**_kwargs)
        return result

    def make_admin_user(self, **kwargs):
        result = self.make_user(**kwargs)
        result.is_staff = True
        result.is_superuser = True
        result.save()
        return result

    def make_something(self, model_class, default, **kwargs):
        _kwargs = default.copy()
        _kwargs.update(kwargs)
        return model_class.objects.create(**_kwargs)

    def make_fleet(self, **kwargs):
        default = dict(user=self.make_user(),
                       account_number=self.make_random_number(),
                       provider=self.make_random_string())
        return self.make_something(Fleet, default, **kwargs)

    def make_bill(self, **kwargs):
        default = dict(fleet=self.make_fleet(), invoice='invoices/zaraza.pdf')
        return self.make_something(Bill, default, **kwargs)

    def make_plan(self, **kwargs):
        default = dict()
        return self.make_something(Plan, default, **kwargs)

    def make_datapack(self, **kwargs):
        default = dict()
        return self.make_something(DataPack, default, **kwargs)

    def make_smspack(self, **kwargs):
        default = dict(units=self.make_random_number())
        return self.make_something(SMSPack, default, **kwargs)

    def make_phone(self, **kwargs):
        default = dict(number=self.make_random_number(),
                       user=self.make_user(), plan=self.make_plan())
        return self.make_something(Phone, default, **kwargs)

    def make_consumption(self, **kwargs):
        default = dict(bill=self.make_bill(), phone=self.make_phone(),
                       plan=self.make_plan())
        return self.make_something(Consumption, default, **kwargs)

    def make_penalty(self, **kwargs):
        default = dict(bill=self.make_bill(), plan=self.make_plan())
        return self.make_something(Penalty, default, **kwargs)
