# coding: utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os

from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from itertools import tee, izip

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum
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
from fleetcore.sendbills import BillSummarySender
from fleetusers.models import UserProfile

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def validate_tax(value):
    """Tax value must be a number in the [0, 1) interval."""
    if not (Decimal('0') <= value and value < Decimal('1')):
        raise ValidationError('%r should be in the interval [0, 1)' % value)


class LeaderTriangle(object):

    def __init__(self, leader):
        u = leader.user
        users = list(UserProfile.objects.filter(leader=u)) + [u]
        self.consumptions = self.consumption_set.filter(phone__user__in=users)
        if consumptions:
            self.total = consumptions.aggregate(total=Sum('total'))['total']


class MoneyField(models.DecimalField):
    """Field to store price/money amount values."""
    def __init__(self, *args, **kwargs):
        default = dict(default=Decimal('0'), decimal_places=3, max_digits=10)
        default.update(kwargs)
        super(MoneyField, self).__init__(*args, **default)


class TaxField(models.DecimalField):
    """Field to store a tax value."""
    def __init__(self, *args, **kwargs):
        validators = kwargs.get('validators', [])
        validators.append(validate_tax)
        kwargs['validators'] = validators
        kwargs.setdefault('default', Decimal('0'))
        kwargs.setdefault('decimal_places', 5)
        kwargs.setdefault('max_digits', 6)
        super(TaxField, self).__init__(*args, **kwargs)


class MinuteField(models.DecimalField):
    """Field to store a minutes value."""
    def __init__(self, *args, **kwargs):
        default = dict(default=Decimal('0'), decimal_places=2, max_digits=10)
        default.update(kwargs)
        super(MinuteField, self).__init__(*args, **default)


class SMSField(models.PositiveIntegerField):
    """Field to store a SMS units value."""
    def __init__(self, *args, **kwargs):
        default = dict(default=0)
        default.update(kwargs)
        super(SMSField, self).__init__(*args, **default)


class Fleet(models.Model):
    """Phones fleet."""
    user = models.ForeignKey(User)
    account_number = models.PositiveIntegerField()
    email = models.EmailField()
    provider = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s - %s' % (self.provider, self.account_number)


class Bill(models.Model):
    """Monthly bill for a fleet."""
    fleet = models.ForeignKey(Fleet)
    invoice = models.FileField(upload_to='invoices')
    billing_date = models.DateField(null=True, blank=True)
    billing_total = MoneyField()
    billing_debt = MoneyField()
    parsing_date = models.DateTimeField(null=True, blank=True)
    upload_date = models.DateTimeField(default=datetime.now)
    provider_number = models.CharField(max_length=50, blank=True)
    internal_tax = TaxField(default=Decimal('0.0417'))
    iva_tax = TaxField(default=Decimal('0.27'))
    other_tax = TaxField(default=Decimal('0.04'))

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

    @property
    def consumptions_total(self):
        return self.consumption_set.aggregate(total=Sum('total'))['total']

    @property
    def outcome(self):
        return self.consumptions_total - self.billing_debt

    @property
    def details(self, user=None):
        if user is None:
            user = User.objects.get(is_superuser=True)

        # group consumptions per leader
        data = {}
        leaders = UserProfile.objects.filter(leader=user)
        for leader in leaders:
            u = leader.user
            users = list(UserProfile.objects.filter(leader=u)) + [u]
            consumptions = self.consumption_set.filter(phone__user__in=users)
            if consumptions:
                total = consumptions.aggregate(total=Sum('total'))['total']
                data[u] = {
                    'consumptions': consumptions,
                    'total': total,
                }

        return data

    def __unicode__(self):
        return 'Bill "%s" (date: %s)' % (self.fleet, self.billing_date)

    def _apply_penalty(self, consumptions, penalty_min, plan_mins):
        assert penalty_min > 0 and consumptions.count() > 1

        # prioritize readable code over efficient code
        data = defaultdict(list)
        for c in consumptions:
            # group by used minutes
            data[c.total_min].append(c)

        # need to add an extra key for the plan total, so when building
        # the pairwise generator, the last total has an entry of its own
        # Example: if we have consumptions to apply penalty to of
        # 30, 50, 80 and the plan target is 100, we need the following pairs:
        # [(30, 50), (50, 80), (80, 100)]
        data[plan_mins].append(None)

        # sort ascending
        totals = pairwise(sorted(data.iterkeys()))
        for total1, total2 in totals:
            # distribute penalty minutes within the same category
            cons = data[total1]
            len_cons = len(cons)

            diff = total2 - total1
            assert diff > 0  # because the key are ascendingly sorted

            to_apply = min(diff * len_cons, penalty_min)
            penalty_min -= to_apply

            to_apply = to_apply / len_cons
            for c in cons:
                c.penalty_min = c.penalty_min + to_apply
                c.save()
                assert penalty_min == 0 or c.total_min == total2

            if penalty_min > 0:
                # update data
                data[total2].extend(cons)
            else:
                # penalty was fully applied
                return

    def apply_penalty(self, consumptions, penalty):
        plan_mins = penalty.plan.included_min
        penalty_min = penalty.minutes
        assert penalty_min > 0 and plan_mins > 0

        # filter those consumptions with unused minutes from the plan total
        consumptions = consumptions.filter(total_min__lt=plan_mins)

        amount = consumptions.count()
        if amount == 0:
            logging.warning('There is no consumption to apply the %s to.',
                            penalty)
        elif amount == 1:
            c = consumptions.get()
            assert c.total_min + penalty_min <= plan_mins
            c.penalty_min = penalty_min
            c.save()
        else:
            self._apply_penalty(consumptions, penalty_min, plan_mins)

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
        self.billing_debt = data.get('bill_debt', Decimal('0'))
        self.billing_total = data.get('bill_total', Decimal('0'))
        self.parsing_date = datetime.now()
        self.provider_number = data.get('bill_number', '')
        self.save()

    def calculate_penalties(self):
        """Calculate penalties per plan with clearing."""
        if self.parsing_date is None:
            raise Bill.AdjustmentError('Bill must be parsed before making '
                                       'adjustments.')

        plans = Plan.objects.filter(phone__consumption__bill=self,
                                    with_min_clearing=True).distinct()
        for plan in plans:
            if Penalty.objects.filter(bill=self, plan=plan).count() > 0:
                logging.warning('Penalty for "%s" and "%s" already exists.',
                                self, plan)
                continue

            consumptions = self.consumption_set.filter(phone__plan=plan)
            if not consumptions:
                logging.info('There is no consumptions for "%s" and "%s".',
                             self, plan)
                continue

            target = plan.included_min * consumptions.count()
            real = consumptions.aggregate(mins=Sum('total_min'))['mins']
            if real < target:
                penalty = Penalty.objects.create(bill=self, plan=plan,
                                                 minutes=target - real)
                self.apply_penalty(consumptions, penalty)

    def notify_users(self):
        """Notify users about this bill."""
        sender = BillSummarySender(billd=self)
        sender.send_mails()


class Plan(models.Model):
    """Phone line plan."""
    name = models.CharField(max_length=100)
    price = MoneyField()
    price_min = MoneyField()
    price_sms = MoneyField()
    included_min = models.PositiveIntegerField(default=0)
    included_sms = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    with_min_clearing = models.BooleanField(default=True)
    # SMS clearing: unused and untested -- for completeness sake
    with_sms_clearing = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - $%s' % (self.name, self.price)


class DataPack(models.Model):
    """Internet data pack."""
    kbs = models.PositiveIntegerField(blank=True, null=True)
    price = MoneyField()

    def __unicode__(self):
        kbs = '%s kbs' % self.kbs if self.kbs else '(unlimited)'
        return '%s - $%s' % (kbs, self.price)


class SMSPack(models.Model):
    """SMS pack."""
    units = SMSField()
    price = MoneyField()

    def __unicode__(self):
        return '%s sms - $%s' % (self.units, self.price)


class Phone(models.Model):
    """Phone line."""
    number = models.PositiveIntegerField()
    user = models.OneToOneField(User)
    plan = models.ForeignKey(Plan)
    data_pack = models.ForeignKey(DataPack, blank=True, null=True)
    sms_pack = models.ForeignKey(SMSPack, blank=True, null=True)
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
    """Phone line consumption for a bill."""
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
    penalty_min = MinuteField('Multa de minutos')
    penalty_sms = SMSField('Multa de mensajes')
    total_min = MinuteField('Suma de minutos consumidos y excedentes, '
                            'y multas')
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
        self.total_min = (self.included_min + self.exceeded_min +
                          self.penalty_min)

        total = self.reported_total
        plan = self.phone.plan
        if plan.with_min_clearing:
            total -= self.monthly_price
            total += self.total_min * plan.price_min
        else:
            total = self.monthly_price

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
    """Penalty to be charged to phone lines in a plan for a bill."""
    bill = models.ForeignKey(Bill)
    plan = models.ForeignKey(Plan)
    minutes = MinuteField()
    sms = SMSField()

    class Meta:
        unique_together = ('bill', 'plan')

    def __unicode__(self):
        return 'Penalty of %s minutes for %s (%s)' % (self.minutes, self.bill,
                                                      self.plan)
