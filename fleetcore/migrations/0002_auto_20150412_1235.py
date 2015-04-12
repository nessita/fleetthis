# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fleetcore.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fleetcore', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='invoice_format',
        ),
        migrations.AlterField(
            model_name='bill',
            name='internal_tax',
            field=fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, default=Decimal('0.0417'), max_digits=6),
        ),
        migrations.AlterField(
            model_name='bill',
            name='iva_tax',
            field=fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, default=Decimal('0.27'), max_digits=6),
        ),
        migrations.AlterField(
            model_name='bill',
            name='other_tax',
            field=fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, default=Decimal('0.04'), max_digits=6),
        ),
        migrations.AlterField(
            model_name='consumption',
            name='taxes',
            field=fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, default=Decimal('0'), max_digits=6),
        ),
    ]
