# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fleet'
        db.create_table('fleetcore_fleet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('account_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('report_consumption_template', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('fleetcore', ['Fleet'])

        # Adding model 'Bill'
        db.create_table('fleetcore_bill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fleet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.Fleet'])),
            ('invoice', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('invoice_format', self.gf('django.db.models.fields.CharField')(default=u'new', max_length=3)),
            ('billing_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('billing_total', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('billing_debt', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('parsing_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('provider_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('internal_tax', self.gf('fleetcore.fields.TaxField')(default='0.0417', max_digits=6, decimal_places=5)),
            ('iva_tax', self.gf('fleetcore.fields.TaxField')(default='0.27', max_digits=6, decimal_places=5)),
            ('other_tax', self.gf('fleetcore.fields.TaxField')(default='0.04', max_digits=6, decimal_places=5)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('fleetcore', ['Bill'])

        # Adding model 'Plan'
        db.create_table('fleetcore_plan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('price_min', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('price_sms', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('included_min', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('included_sms', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('with_min_clearing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('with_sms_clearing', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('fleetcore', ['Plan'])

        # Adding model 'DataPack'
        db.create_table('fleetcore_datapack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kbs', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
        ))
        db.send_create_signal('fleetcore', ['DataPack'])

        # Adding model 'SMSPack'
        db.create_table('fleetcore_smspack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('units', self.gf('fleetcore.fields.SMSField')(default=0)),
            ('price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
        ))
        db.send_create_signal('fleetcore', ['SMSPack'])

        # Adding model 'Phone'
        db.create_table('fleetcore_phone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.Plan'])),
            ('data_pack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.DataPack'], null=True, blank=True)),
            ('sms_pack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.SMSPack'], null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('active_since', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 2, 0, 0))),
            ('active_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('fleetcore', ['Phone'])

        # Adding model 'Consumption'
        db.create_table('fleetcore_consumption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.Phone'])),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.Bill'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.Plan'])),
            ('reported_user', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('reported_plan', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('monthly_price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('services', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('refunds', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('included_min', self.gf('fleetcore.fields.MinuteField')(default='0', max_digits=10, decimal_places=2)),
            ('exceeded_min', self.gf('fleetcore.fields.MinuteField')(default='0', max_digits=10, decimal_places=2)),
            ('exceeded_min_price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('ndl_min', self.gf('fleetcore.fields.MinuteField')(default='0', max_digits=10, decimal_places=2)),
            ('ndl_min_price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('idl_min', self.gf('fleetcore.fields.MinuteField')(default='0', max_digits=10, decimal_places=2)),
            ('idl_min_price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('sms', self.gf('fleetcore.fields.SMSField')(default=0)),
            ('sms_price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('equipment_price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('other_price', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('reported_total', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('penalty_min', self.gf('fleetcore.fields.MinuteField')(default='0', max_digits=10, decimal_places=2)),
            ('penalty_sms', self.gf('fleetcore.fields.SMSField')(default=0)),
            ('total_min', self.gf('fleetcore.fields.MinuteField')(default='0', max_digits=10, decimal_places=2)),
            ('total_before_taxes', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('taxes', self.gf('fleetcore.fields.TaxField')(default='0', max_digits=6, decimal_places=5)),
            ('total_before_round', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('total', self.gf('fleetcore.fields.MoneyField')(default='0', max_digits=10, decimal_places=3)),
            ('payed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('fleetcore', ['Consumption'])

        # Adding unique constraint on 'Consumption', fields ['phone', 'bill']
        db.create_unique('fleetcore_consumption', ['phone_id', 'bill_id'])

        # Adding model 'Penalty'
        db.create_table('fleetcore_penalty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.Bill'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleetcore.Plan'])),
            ('minutes', self.gf('fleetcore.fields.MinuteField')(default='0', max_digits=10, decimal_places=2)),
            ('sms', self.gf('fleetcore.fields.SMSField')(default=0)),
        ))
        db.send_create_signal('fleetcore', ['Penalty'])

        # Adding unique constraint on 'Penalty', fields ['bill', 'plan']
        db.create_unique('fleetcore_penalty', ['bill_id', 'plan_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Penalty', fields ['bill', 'plan']
        db.delete_unique('fleetcore_penalty', ['bill_id', 'plan_id'])

        # Removing unique constraint on 'Consumption', fields ['phone', 'bill']
        db.delete_unique('fleetcore_consumption', ['phone_id', 'bill_id'])

        # Deleting model 'Fleet'
        db.delete_table('fleetcore_fleet')

        # Deleting model 'Bill'
        db.delete_table('fleetcore_bill')

        # Deleting model 'Plan'
        db.delete_table('fleetcore_plan')

        # Deleting model 'DataPack'
        db.delete_table('fleetcore_datapack')

        # Deleting model 'SMSPack'
        db.delete_table('fleetcore_smspack')

        # Deleting model 'Phone'
        db.delete_table('fleetcore_phone')

        # Deleting model 'Consumption'
        db.delete_table('fleetcore_consumption')

        # Deleting model 'Penalty'
        db.delete_table('fleetcore_penalty')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fleetcore.bill': {
            'Meta': {'object_name': 'Bill'},
            'billing_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'billing_debt': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'billing_total': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.Fleet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_tax': ('fleetcore.fields.TaxField', [], {'default': "'0.0417'", 'max_digits': '6', 'decimal_places': '5'}),
            'invoice': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'invoice_format': ('django.db.models.fields.CharField', [], {'default': "u'new'", 'max_length': '3'}),
            'iva_tax': ('fleetcore.fields.TaxField', [], {'default': "'0.27'", 'max_digits': '6', 'decimal_places': '5'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'other_tax': ('fleetcore.fields.TaxField', [], {'default': "'0.04'", 'max_digits': '6', 'decimal_places': '5'}),
            'parsing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'provider_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'fleetcore.consumption': {
            'Meta': {'ordering': "(u'phone',)", 'unique_together': "((u'phone', u'bill'),)", 'object_name': 'Consumption'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.Bill']"}),
            'equipment_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'exceeded_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'exceeded_min_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idl_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'idl_min_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'included_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'monthly_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'ndl_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'ndl_min_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'other_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'payed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'penalty_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'penalty_sms': ('fleetcore.fields.SMSField', [], {'default': '0'}),
            'phone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.Phone']"}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.Plan']"}),
            'refunds': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'reported_plan': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'reported_total': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'reported_user': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'services': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'sms': ('fleetcore.fields.SMSField', [], {'default': '0'}),
            'sms_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'taxes': ('fleetcore.fields.TaxField', [], {'default': "'0'", 'max_digits': '6', 'decimal_places': '5'}),
            'total': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'total_before_round': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'total_before_taxes': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'total_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'})
        },
        'fleetcore.datapack': {
            'Meta': {'object_name': 'DataPack'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kbs': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'})
        },
        'fleetcore.fleet': {
            'Meta': {'object_name': 'Fleet'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'report_consumption_template': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'fleetcore.penalty': {
            'Meta': {'unique_together': "((u'bill', u'plan'),)", 'object_name': 'Penalty'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.Plan']"}),
            'sms': ('fleetcore.fields.SMSField', [], {'default': '0'})
        },
        'fleetcore.phone': {
            'Meta': {'object_name': 'Phone'},
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)'}),
            'active_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'data_pack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.DataPack']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.Plan']"}),
            'sms_pack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fleetcore.SMSPack']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'fleetcore.plan': {
            'Meta': {'object_name': 'Plan'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_min': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'included_sms': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'price_min': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'price_sms': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'with_min_clearing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'with_sms_clearing': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'fleetcore.smspack': {
            'Meta': {'object_name': 'SMSPack'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'units': ('fleetcore.fields.SMSField', [], {'default': '0'})
        }
    }

    complete_apps = ['fleetcore']