# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fleetcore.fields
import django.utils.timezone
from django.conf import settings
from decimal import Decimal
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleetUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'}, unique=True, verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True)),
                ('leader', models.ForeignKey(related_name='leadering', to=settings.AUTH_USER_MODEL, null=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('invoice', models.FileField(upload_to='invoices')),
                ('invoice_format', models.CharField(max_length=3, choices=[('new', 'New'), ('old', 'Old')], default='new')),
                ('billing_date', models.DateField(null=True, blank=True)),
                ('billing_total', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('billing_debt', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('parsing_date', models.DateTimeField(null=True, blank=True)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('provider_number', models.CharField(max_length=50, blank=True)),
                ('internal_tax', fleetcore.fields.TaxField(max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0.0417'))),
                ('iva_tax', fleetcore.fields.TaxField(max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0.27'))),
                ('other_tax', fleetcore.fields.TaxField(max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0.04'))),
                ('notes', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('reported_user', models.CharField(max_length=500, verbose_name='Usuario', blank=True)),
                ('reported_plan', models.CharField(max_length=5, verbose_name='Plan oficial', blank=True)),
                ('monthly_price', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Precio del plan ($)', default=Decimal('0'))),
                ('services', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Cargos y servicios ($)', default=Decimal('0'))),
                ('refunds', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Reintegros ($)', default=Decimal('0'))),
                ('included_min', fleetcore.fields.MinuteField(max_digits=10, decimal_places=2, verbose_name='Minutos consumidos incluidos en plan', default=Decimal('0'))),
                ('exceeded_min', fleetcore.fields.MinuteField(max_digits=10, decimal_places=2, verbose_name='Minutos consumidos fuera del plan', default=Decimal('0'))),
                ('exceeded_min_price', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Minutos consumidos fuera del plan ($)', default=Decimal('0'))),
                ('ndl_min', fleetcore.fields.MinuteField(max_digits=10, decimal_places=2, verbose_name='Discado nacional (minutos)', default=Decimal('0'))),
                ('ndl_min_price', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Discado nacional ($)', default=Decimal('0'))),
                ('idl_min', fleetcore.fields.MinuteField(max_digits=10, decimal_places=2, verbose_name='Discado internacional (minutos)', default=Decimal('0'))),
                ('idl_min_price', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Discado internacional ($)', default=Decimal('0'))),
                ('sms', fleetcore.fields.SMSField(verbose_name='Mensajes consumidos', default=0)),
                ('sms_price', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Mensajes consumidos ($)', default=Decimal('0'))),
                ('equipment_price', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Equipos ($)', default=Decimal('0'))),
                ('other_price', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Varios ($)', default=Decimal('0'))),
                ('reported_total', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Total ($)', default=Decimal('0'))),
                ('penalty_min', fleetcore.fields.MinuteField(max_digits=10, decimal_places=2, verbose_name='Multa de minutos', default=Decimal('0'))),
                ('penalty_sms', fleetcore.fields.SMSField(verbose_name='Multa de mensajes', default=0)),
                ('mins', fleetcore.fields.MinuteField(max_digits=10, decimal_places=2, verbose_name='Suma de minutos consumidos y excedentes, antes de multas', default=Decimal('0'))),
                ('total_before_taxes', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('taxes', fleetcore.fields.TaxField(max_digits=6, decimal_places=5, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], default=Decimal('0'))),
                ('total_before_round', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('total', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('extra', fleetcore.fields.MoneyField(max_digits=10, decimal_places=3, verbose_name='Extra (por equipo/s, o IVA de equipo, etc.)', default=Decimal('0'))),
                ('bill', models.ForeignKey(to='fleetcore.Bill')),
            ],
            options={
                'get_latest_by': 'bill__billing_date',
            },
        ),
        migrations.CreateModel(
            name='DataPack',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('kbs', models.PositiveIntegerField(null=True, blank=True)),
                ('price', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
            ],
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('account_number', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('provider', models.CharField(max_length=256)),
                ('report_consumption_template', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('minutes', fleetcore.fields.MinuteField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('sms', fleetcore.fields.SMSField(default=0)),
                ('bill', models.ForeignKey(to='fleetcore.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('notes', models.TextField(blank=True)),
                ('active_since', models.DateTimeField(default=django.utils.timezone.now)),
                ('active_to', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'get_latest_by': 'active_since',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('price_min', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('price_sms', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('included_min', models.PositiveIntegerField(default=0)),
                ('included_sms', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('with_min_clearing', models.BooleanField(default=True)),
                ('with_sms_clearing', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SMSPack',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('units', fleetcore.fields.SMSField(default=0)),
                ('price', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
            ],
        ),
        migrations.AddField(
            model_name='phone',
            name='current_plan',
            field=models.ForeignKey(to='fleetcore.Plan'),
        ),
        migrations.AddField(
            model_name='phone',
            name='data_pack',
            field=models.ForeignKey(to='fleetcore.DataPack', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='phone',
            name='sms_pack',
            field=models.ForeignKey(to='fleetcore.SMSPack', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='phone',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='penalty',
            name='plan',
            field=models.ForeignKey(to='fleetcore.Plan'),
        ),
        migrations.AddField(
            model_name='consumption',
            name='phone',
            field=models.ForeignKey(to='fleetcore.Phone'),
        ),
        migrations.AddField(
            model_name='consumption',
            name='plan',
            field=models.ForeignKey(to='fleetcore.Plan'),
        ),
        migrations.AddField(
            model_name='bill',
            name='fleet',
            field=models.ForeignKey(to='fleetcore.Fleet'),
        ),
        migrations.AlterUniqueTogether(
            name='penalty',
            unique_together=set([('bill', 'plan')]),
        ),
        migrations.AlterUniqueTogether(
            name='consumption',
            unique_together=set([('phone', 'bill')]),
        ),
    ]
