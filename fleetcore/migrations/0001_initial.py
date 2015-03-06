# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
from decimal import Decimal
import fleetcore.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleetUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', related_name='user_set', verbose_name='groups', to='auth.Group', blank=True)),
                ('leader', models.ForeignKey(related_name='leadering', to=settings.AUTH_USER_MODEL, null=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', related_name='user_set', verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('invoice', models.FileField(upload_to='invoices')),
                ('invoice_format', models.CharField(choices=[('new', 'New'), ('old', 'Old')], max_length=3, default='new')),
                ('billing_date', models.DateField(blank=True, null=True)),
                ('billing_total', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('billing_debt', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('parsing_date', models.DateTimeField(blank=True, null=True)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('provider_number', models.CharField(max_length=50, blank=True)),
                ('internal_tax', fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, max_digits=6, default=Decimal('0.0417'))),
                ('iva_tax', fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, max_digits=6, default=Decimal('0.27'))),
                ('other_tax', fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, max_digits=6, default=Decimal('0.04'))),
                ('notes', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('reported_user', models.CharField(max_length=500, verbose_name='Usuario', blank=True)),
                ('reported_plan', models.CharField(max_length=5, verbose_name='Plan oficial', blank=True)),
                ('monthly_price', fleetcore.fields.MoneyField(verbose_name='Precio del plan ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('services', fleetcore.fields.MoneyField(verbose_name='Cargos y servicios ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('refunds', fleetcore.fields.MoneyField(verbose_name='Reintegros ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('included_min', fleetcore.fields.MinuteField(verbose_name='Minutos consumidos incluidos en plan', decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('exceeded_min', fleetcore.fields.MinuteField(verbose_name='Minutos consumidos fuera del plan', decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('exceeded_min_price', fleetcore.fields.MoneyField(verbose_name='Minutos consumidos fuera del plan ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('ndl_min', fleetcore.fields.MinuteField(verbose_name='Discado nacional (minutos)', decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('ndl_min_price', fleetcore.fields.MoneyField(verbose_name='Discado nacional ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('idl_min', fleetcore.fields.MinuteField(verbose_name='Discado internacional (minutos)', decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('idl_min_price', fleetcore.fields.MoneyField(verbose_name='Discado internacional ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('sms', fleetcore.fields.SMSField(verbose_name='Mensajes consumidos', default=0)),
                ('sms_price', fleetcore.fields.MoneyField(verbose_name='Mensajes consumidos ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('equipment_price', fleetcore.fields.MoneyField(verbose_name='Equipos ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('other_price', fleetcore.fields.MoneyField(verbose_name='Varios ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('reported_total', fleetcore.fields.MoneyField(verbose_name='Total ($)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('penalty_min', fleetcore.fields.MinuteField(verbose_name='Multa de minutos', decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('penalty_sms', fleetcore.fields.SMSField(verbose_name='Multa de mensajes', default=0)),
                ('mins', fleetcore.fields.MinuteField(verbose_name='Suma de minutos consumidos y excedentes, antes de multas', decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('total_before_taxes', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('taxes', fleetcore.fields.TaxField(validators=[fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax, fleetcore.fields.validate_tax], decimal_places=5, max_digits=6, default=Decimal('0'))),
                ('total_before_round', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('total', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('extra', fleetcore.fields.MoneyField(verbose_name='Extra (por equipo/s, o IVA de equipo, etc.)', decimal_places=3, max_digits=10, default=Decimal('0'))),
                ('bill', models.ForeignKey(to='fleetcore.Bill')),
            ],
            options={
                'get_latest_by': 'bill__billing_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataPack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('kbs', models.PositiveIntegerField(blank=True, null=True)),
                ('price', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('account_number', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=75)),
                ('provider', models.CharField(max_length=100)),
                ('report_consumption_template', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('minutes', fleetcore.fields.MinuteField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('sms', fleetcore.fields.SMSField(default=0)),
                ('bill', models.ForeignKey(to='fleetcore.Bill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.PositiveIntegerField()),
                ('notes', models.TextField(blank=True)),
                ('active_since', models.DateTimeField(default=django.utils.timezone.now)),
                ('active_to', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'get_latest_by': 'active_since',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMSPack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('units', fleetcore.fields.SMSField(default=0)),
                ('price', fleetcore.fields.MoneyField(decimal_places=3, max_digits=10, default=Decimal('0'))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='phone',
            name='current_plan',
            field=models.ForeignKey(to='fleetcore.Plan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phone',
            name='data_pack',
            field=models.ForeignKey(to='fleetcore.DataPack', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phone',
            name='sms_pack',
            field=models.ForeignKey(to='fleetcore.SMSPack', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phone',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='penalty',
            name='plan',
            field=models.ForeignKey(to='fleetcore.Plan'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='penalty',
            unique_together=set([('bill', 'plan')]),
        ),
        migrations.AddField(
            model_name='consumption',
            name='phone',
            field=models.ForeignKey(to='fleetcore.Phone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consumption',
            name='plan',
            field=models.ForeignKey(to='fleetcore.Plan'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='consumption',
            unique_together=set([('phone', 'bill')]),
        ),
        migrations.AddField(
            model_name='bill',
            name='fleet',
            field=models.ForeignKey(to='fleetcore.Fleet'),
            preserve_default=True,
        ),
    ]
