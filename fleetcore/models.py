# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import os

from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save

from fleetcore import pdf2cell
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


def validate_tax(value):
    if not (Decimal('0') <= value and value < Decimal('1')):
        raise ValidationError('%r should be in the interval [0, 1)' % value)


class MoneyField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        default = dict(default=Decimal('0'), decimal_places=3, max_digits=10)
        default.update(kwargs)
        super(MoneyField, self).__init__(*args, **default)


class TaxField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        validators = kwargs.get('validators', [])
        validators.append(validate_tax)
        kwargs['validators'] = validators
        kwargs.setdefault('default', Decimal('0'))
        kwargs.setdefault('decimal_places', 5)
        kwargs.setdefault('max_digits', 6)
        super(TaxField, self).__init__(*args, **kwargs)


class MinuteField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        default = dict(default=Decimal('0'), decimal_places=2, max_digits=10)
        default.update(kwargs)
        super(MinuteField, self).__init__(*args, **default)


class SMSField(models.PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        default = dict(default=0)
        default.update(kwargs)
        super(SMSField, self).__init__(*args, **default)


class Fleet(models.Model):
    user = models.ForeignKey(User)
    account_number = models.PositiveIntegerField()
    email = models.EmailField()
    provider = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s - %s' % (self.provider, self.account_number)


class Bill(models.Model):
    fleet = models.ForeignKey(Fleet)
    invoice = models.FileField(upload_to='invoices')
    billing_date = models.DateField(null=True, blank=True)
    parsing_date = models.DateTimeField(null=True, blank=True)
    upload_date = models.DateTimeField(default=datetime.now)
    provider_number = models.CharField(max_length=50, blank=True)
    internal_tax = TaxField(default=Decimal('0.0417'))
    iva_tax = TaxField(default=Decimal('0.27'))
    other_tax = TaxField(default=Decimal('0.01'))

    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class ParseError(Exception):
        """The invoice could not be parsed."""

    class AdjustmentError(Exception):
        """The invoice could not be adjusted."""

    class NotifyError(Exception):
        """The users could not be notified."""

    @property
    def taxes(self):
        return self.internal_tax + self.iva_tax + self.other_tax

    def __unicode__(self):
        return 'Bill for "%s" (date: %s)' % (self.fleet, self.billing_date)

    @transaction.commit_on_success
    def parse_invoice(self):
        """Parse this bill's invoice.

        Return whether the parse was successful

        """
        if self.parsing_date is not None:
            raise Bill.ParseError('Invoice already parsed on %s.' %
                                  self.parsing_date)

        try:
            fname = self.invoice.path
        except ValueError:
            raise Bill.ParseError('Invoice path can not be loaded.')

        if not os.path.exists(fname):
            raise Bill.ParseError('Invoice path does not exist.')

        data = pdf2cell.parse_file(fname)
        for d in data.get('phone_data', []):
            try:
                phone = Phone.objects.get(number=d[PHONE_NUMBER])
            except Phone.DoesNotExist:
                raise Bill.ParseError('Phone %s does not exist.' %
                                      d[PHONE_NUMBER])
            kwargs = dict(
                reported_user=d[USER],
                reported_plan=d[PLAN],
                monthly_price=d[MONTHLY_PRICE],
                services=d[SERVICES],
                refunds=d[REFUNDS],
                included_min=d[INCLUDED_MIN],
                exceeded_min=d[EXCEEDED_MIN],
                exceeded_min_price=d[EXCEEDED_MIN_PRICE],
                ndl_min=d[NDL_MIN],
                ndl_min_price=d[NDL_PRICE],
                idl_min=d[IDL_MIN],
                idl_min_price=d[IDL_PRICE],
                sms=d[SMS],
                sms_price=d[SMS_PRICE],
                equipment_price=d[EQUIPMENT_PRICE],
                other_price=d[OTHER_PRICE],
                reported_total=d[TOTAL_PRICE],
            )
            Consumption.objects.create(phone=phone, bill=self, **kwargs)

        bill_date = data.get('bill_date')
        if bill_date:
            self.billing_date = bill_date
        self.parsing_date = datetime.now()
        self.provider_number = data.get('bill_number', '')
        self.save()

    def make_adjustments(self):
        """Make all the required adjustment to Consumptions."""
        if self.parsing_date is None:
            raise Bill.AdjustmentError('Bill must be parsed before making '
                                       'adjustments.')

        #for c in self.consumption_set.all():
        #    print(c)

    def notify_users(self):
        """Notify users about this bill."""


class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = MoneyField()
    min_price = MoneyField()
    sms_price = MoneyField()
    included_minutes = models.PositiveIntegerField(default=0)
    included_sms = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    with_min_clearing = models.BooleanField(default=True)
    # SMS clearing: unused and untested -- for completeness sake
    with_sms_clearing = models.BooleanField(default=False)

    def __unicode__(self):
        min_clearing = ('with' if self.with_min_clearing else 'no' +
                        'clearing for minutes')
        sms_clearing = ('with' if self.with_sms_clearing else 'no' +
                        'clearing for sms')
        return '%s - $%s (%s, %s)' % (self.name, self.price,
                                      min_clearing, sms_clearing)


class Phone(models.Model):
    number = models.PositiveIntegerField()
    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    notes = models.TextField(blank=True)
    active_since = models.DateTimeField(default=datetime.today)
    active_to = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        result = unicode(self.number)
        if self.user.get_full_name():
            result += ' - %s' % self.user.get_full_name()
        return result

    @property
    def active(self):
        return self.active_to is None or self.active_to > datetime.now()


class Consumption(models.Model):
    phone = models.ForeignKey(Phone)
    bill = models.ForeignKey(Bill)

    # every field (literal) from the invoice
    reported_user = models.CharField('Usuario', max_length=500, blank=True)
    reported_plan = models.CharField('Plan', max_length=100, blank=True)
    monthly_price = MoneyField('Precio del plan ($)')
    services = MoneyField('Cargos y servicios ($)')
    refunds = MoneyField('Reintegros ($)')
    included_min = MinuteField('Minutos consumidos incluidos en plan')
    exceeded_min = MinuteField('Minutos consumidos fuera del plan')
    exceeded_min_price = MoneyField('Minutos consumidos fuera del plan ($)')
    ndl_min = MinuteField('Discado nacional (minutos)')
    ndl_min_price = MoneyField('Discado nacional ($)')
    idl_min = MinuteField('Discado internacional (minutos)')
    idl_min_price = MoneyField('Discado internacional ($)')
    sms = SMSField('Mensajes consumidos')
    sms_price = MoneyField('Mensajes consumidos ($)')
    equipment_price = MoneyField('Equipos ($)')
    other_price = MoneyField('Varios ($)')
    reported_total = MoneyField('Total ($)')

    # calculated *and* stored in the DB
    min_penalty = MinuteField('Multa de minutos')
    sms_penalty = SMSField('Multa de mensajes')
    total_before_taxes = MoneyField()
    taxes = TaxField()
    total_before_round = MoneyField()
    total = MoneyField()

    # keep track of the payment of this consumption
    payed = models.BooleanField()

    def __unicode__(self):
        return '%s - Bill from %s - Phone %s' % (self.bill.fleet.provider,
                                                 self.bill.billing_date,
                                                 self.phone)

    def save(self, *args, **kwargs):
        total = self.reported_total
        plan = self.phone.plan
        if plan.with_min_clearing:
            total -= self.monthly_price
            total += plan.included_minutes * plan.min_price
        else:
            total = self.monthly_price

        # XXX: missing: add non-consumed minutes if aplicable

        self.total_before_taxes = total
        self.taxes = self.bill.taxes
        self.total_before_round = (self.total_before_taxes *
                                   (Decimal('1') + self.taxes))
        self.total = round(self.total_before_round)
        super(Consumption, self).save(*args, **kwargs)

    class Meta:
        ordering = ('phone',)
        get_latest_by = 'bill__billing_date'
        unique_together = ('phone', 'bill')


class Penalty(models.Model):

    bill = models.ForeignKey(Bill)
    plan = models.ForeignKey(Plan)
    minutes = MinuteField()
    sms = SMSField()
