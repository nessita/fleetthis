# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fleetcore.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fleetcore', '0003_auto_20150412_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='internal_tax',
            field=fleetcore.fields.TaxField(max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0.0417'), decimal_places=5),
        ),
        migrations.AlterField(
            model_name='bill',
            name='iva_tax',
            field=fleetcore.fields.TaxField(max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0.27'), decimal_places=5),
        ),
        migrations.AlterField(
            model_name='bill',
            name='other_tax',
            field=fleetcore.fields.TaxField(max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0.04'), decimal_places=5),
        ),
        migrations.AlterField(
            model_name='consumption',
            name='taxes',
            field=fleetcore.fields.TaxField(max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0'), decimal_places=5),
        ),
    ]
