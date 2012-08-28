from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from fleetthis.fleetcore import pdf2cell
from fleetthis.fleetcore.pdf2cell import (
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


class Plan(models.Model):
    name = models.CharField(max_length=100)
    with_clearing = models.BooleanField()
    price = MoneyField()
    min_price = MoneyField()
    sms_price = MoneyField()
    included_minutes = models.PositiveIntegerField()
    included_sms = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s - $%s' % (self.name, self.price)


class Phone(models.Model):
    number = models.PositiveIntegerField()
    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.number, self.user)


class Fleet(models.Model):
    owner = models.ForeignKey(User)
    account_number = models.PositiveIntegerField()
    email = models.EmailField()
    provider = models.CharField(max_length=100)

    def __unicode__(self):
        return u'Fleet %s - %s' % (self.provider, self.account_number)


class Bill(models.Model):
    fleet = models.ForeignKey(Fleet)
    invoice = models.FileField(upload_to='invoices')
    billing_date = models.DateField()  # billing date
    internal_tax = TaxField(default=Decimal('0.0417'))
    iva_tax = TaxField(default=Decimal('0.27'))
    other_tax = TaxField(default=Decimal('0.01'))

    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    @property
    def taxes(self):
        return self.internal_tax + self.iva_tax + self.other_tax

    def __unicode__(self):
        return u'Bill %s (%s)' % (self.billing_date, self.fleet)


class Consumption(models.Model):
    phone = models.ForeignKey(Phone)
    bill = models.ForeignKey(Bill)

    # every field (literal) from the invoice
    reported_user = models.CharField(max_length=500, blank=True)
    reported_plan = models.CharField(max_length=100, blank=True)
    monthly_price = MoneyField()
    services = MoneyField()
    refunds = MoneyField()
    included_min = MinuteField()
    exceeded_min = MinuteField()
    exceeded_min_price = MoneyField()
    ndl_min = MinuteField()
    ndl_min_price = MoneyField()
    idl_min = MinuteField()
    idl_min_price = MoneyField()
    sms = models.PositiveIntegerField(default=0)
    sms_price = MoneyField()
    equipment_price = MoneyField()
    other_price = MoneyField()
    reported_total = MoneyField()

    # calculated *and* stored in the DB
    total_before_taxes = MoneyField()
    taxes = TaxField()
    total_before_round = MoneyField()
    total = MoneyField()

    # keep track of the payment of this consumption
    payed = models.BooleanField()

    def __unicode__(self):
        return self.period

    def save(self, *args, **kwargs):
        if self.phone.plan.is_clearing:
            total = self.reported_total - self.monthly_price
            total += self.included_minutes * phone.plan.minute_price
        else:
            total = self.monthly_price

        # XXX: missing: add non-consumed minutes if aplicable

        self.total_before_taxes = total
        self.taxes = self.bill.taxes
        self.total_before_round = (self.total_before_taxes *
                                   (Decimal('1') + taxes))
        self.total = round(self.total_before_round)
        super(Consumption, self).save(*args, **kwargs)

    class Meta:
        ordering = ('phone',)
        get_latest_by = 'bill__billing_date'
        unique_together = ('phone', 'bill')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    leader = models.ForeignKey(User, related_name='leadered_by', null=True)
    fleet = models.ForeignKey(Fleet, null=True)


def parse_invoice(bill):
    # parse invoice
    fname = bill.invoice.path
    data = pdf2cell.parse_file(fname)
    for d in data:
        phone = Phone.objects.get(number=d[PHONE_NUMBER])
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
        Consumption.objects.create(phone=phone, bill=bill, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def process_bill(sender, instance, created, **kwargs):
    if created:
        parse_invoice(instance)


post_save.connect(create_user_profile, sender=User)
post_save.connect(process_bill, sender=Bill)
