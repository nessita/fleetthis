# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fleetcore.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fleetcore', '0002_auto_20150412_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='invoice_filename',
            field=models.CharField(max_length=512, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='internal_tax',
            field=fleetcore.fields.TaxField(default=Decimal('0.0417'), max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='iva_tax',
            field=fleetcore.fields.TaxField(default=Decimal('0.27'), max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='other_tax',
            field=fleetcore.fields.TaxField(default=Decimal('0.04'), max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax]),
        ),
        migrations.AlterField(
            model_name='consumption',
            name='taxes',
            field=fleetcore.fields.TaxField(default=Decimal('0'), max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax]),
        ),
    ]
