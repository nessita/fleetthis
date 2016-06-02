from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class MoneyField(models.DecimalField):
    """Field to store price/money amount values."""
    def __init__(self, *args, **kwargs):
        default = dict(default=Decimal('0'), decimal_places=3, max_digits=10)
        default.update(kwargs)
        super(MoneyField, self).__init__(*args, **default)


def validate_tax(value):
    """Tax value must be a number in the [0, 1) interval."""
    if not (Decimal('0') <= value and value < Decimal('1')):
        raise ValidationError('%r should be in the interval [0, 1)' % value)


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
