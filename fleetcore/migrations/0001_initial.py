# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models
from decimal import Decimal
import django.utils.timezone
import fleetcore.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleetUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], max_length=30, error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', blank=True, to='auth.Group', related_name='user_set')),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='leadering')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', verbose_name='user permissions', blank=True, to='auth.Permission', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('invoice', models.FileField(upload_to='invoices')),
                ('invoice_format', models.CharField(choices=[('new', 'New'), ('old', 'Old')], default='new', max_length=3)),
                ('billing_date', models.DateField(null=True, blank=True)),
                ('billing_total', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
                ('billing_debt', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
                ('parsing_date', models.DateTimeField(null=True, blank=True)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('provider_number', models.CharField(max_length=50, blank=True)),
                ('internal_tax', fleetcore.fields.TaxField(default=Decimal('0.0417'), max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5)),
                ('iva_tax', fleetcore.fields.TaxField(default=Decimal('0.27'), max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5)),
                ('other_tax', fleetcore.fields.TaxField(default=Decimal('0.04'), max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5)),
                ('notes', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('reported_user', models.CharField(max_length=500, verbose_name='Usuario', blank=True)),
                ('reported_plan', models.CharField(max_length=5, verbose_name='Plan oficial', blank=True)),
                ('monthly_price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Precio del plan ($)', decimal_places=3)),
                ('services', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Cargos y servicios ($)', decimal_places=3)),
                ('refunds', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Reintegros ($)', decimal_places=3)),
                ('included_min', fleetcore.fields.MinuteField(default=Decimal('0'), max_digits=10, verbose_name='Minutos consumidos incluidos en plan', decimal_places=2)),
                ('exceeded_min', fleetcore.fields.MinuteField(default=Decimal('0'), max_digits=10, verbose_name='Minutos consumidos fuera del plan', decimal_places=2)),
                ('exceeded_min_price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Minutos consumidos fuera del plan ($)', decimal_places=3)),
                ('ndl_min', fleetcore.fields.MinuteField(default=Decimal('0'), max_digits=10, verbose_name='Discado nacional (minutos)', decimal_places=2)),
                ('ndl_min_price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Discado nacional ($)', decimal_places=3)),
                ('idl_min', fleetcore.fields.MinuteField(default=Decimal('0'), max_digits=10, verbose_name='Discado internacional (minutos)', decimal_places=2)),
                ('idl_min_price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Discado internacional ($)', decimal_places=3)),
                ('sms', fleetcore.fields.SMSField(default=0, verbose_name='Mensajes consumidos')),
                ('sms_price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Mensajes consumidos ($)', decimal_places=3)),
                ('equipment_price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Equipos ($)', decimal_places=3)),
                ('other_price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Varios ($)', decimal_places=3)),
                ('reported_total', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Total ($)', decimal_places=3)),
                ('penalty_min', fleetcore.fields.MinuteField(default=Decimal('0'), max_digits=10, verbose_name='Multa de minutos', decimal_places=2)),
                ('penalty_sms', fleetcore.fields.SMSField(default=0, verbose_name='Multa de mensajes')),
                ('mins', fleetcore.fields.MinuteField(default=Decimal('0'), max_digits=10, verbose_name='Suma de minutos consumidos y excedentes, antes de multas', decimal_places=2)),
                ('total_before_taxes', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
                ('taxes', fleetcore.fields.TaxField(default=Decimal('0'), max_digits=6, validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5)),
                ('total_before_round', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
                ('total', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
                ('extra', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, verbose_name='Extra (por equipo/s, o IVA de equipo, etc.)', decimal_places=3)),
                ('bill', models.ForeignKey(to='fleetcore.Bill')),
            ],
            options={
                'get_latest_by': 'bill__billing_date',
            },
        ),
        migrations.CreateModel(
            name='DataPack',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('kbs', models.PositiveIntegerField(null=True, blank=True)),
                ('price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('account_number', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('provider', models.CharField(max_length=256)),
                ('report_consumption_template', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('minutes', fleetcore.fields.MinuteField(default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('sms', fleetcore.fields.SMSField(default=0)),
                ('bill', models.ForeignKey(to='fleetcore.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('number', models.CharField(max_length=10)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
                ('price_min', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
                ('price_sms', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('units', fleetcore.fields.SMSField(default=0)),
                ('price', fleetcore.fields.MoneyField(default=Decimal('0'), max_digits=10, decimal_places=3)),
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
            field=models.ForeignKey(blank=True, to='fleetcore.DataPack', null=True),
        ),
        migrations.AddField(
            model_name='phone',
            name='sms_pack',
            field=models.ForeignKey(blank=True, to='fleetcore.SMSPack', null=True),
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
