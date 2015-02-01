# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Consumption.payed'
        db.delete_column(u'fleetcore_consumption', 'payed')


    def backwards(self, orm):
        # Adding field 'Consumption.payed'
        db.add_column(u'fleetcore_consumption', 'payed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fleetcore.bill': {
            'Meta': {'object_name': 'Bill'},
            'billing_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'billing_debt': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'billing_total': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.Fleet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_tax': ('fleetcore.fields.TaxField', [], {'default': "'0.0417'", 'max_digits': '6', 'decimal_places': '5'}),
            'invoice': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'invoice_format': ('django.db.models.fields.CharField', [], {'default': "u'new'", 'max_length': '3'}),
            'iva_tax': ('fleetcore.fields.TaxField', [], {'default': "'0.27'", 'max_digits': '6', 'decimal_places': '5'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'other_tax': ('fleetcore.fields.TaxField', [], {'default': "'0.04'", 'max_digits': '6', 'decimal_places': '5'}),
            'parsing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'provider_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'fleetcore.consumption': {
            'Meta': {'unique_together': "((u'phone', u'bill'),)", 'object_name': 'Consumption'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.Bill']"}),
            'equipment_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'exceeded_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'exceeded_min_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'extra': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idl_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'idl_min_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'included_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'mins': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'monthly_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'ndl_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'ndl_min_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'other_price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'penalty_min': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'penalty_sms': ('fleetcore.fields.SMSField', [], {'default': '0'}),
            'phone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.Phone']"}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.Plan']"}),
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
            'total_before_taxes': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'})
        },
        u'fleetcore.datapack': {
            'Meta': {'object_name': 'DataPack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kbs': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'})
        },
        u'fleetcore.fleet': {
            'Meta': {'object_name': 'Fleet'},
            'account_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'report_consumption_template': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'fleetcore.penalty': {
            'Meta': {'unique_together': "((u'bill', u'plan'),)", 'object_name': 'Penalty'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.Bill']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('fleetcore.fields.MinuteField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.Plan']"}),
            'sms': ('fleetcore.fields.SMSField', [], {'default': '0'})
        },
        u'fleetcore.phone': {
            'Meta': {'object_name': 'Phone'},
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 1, 0, 0)'}),
            'active_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'current_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.Plan']"}),
            'data_pack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.DataPack']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sms_pack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleetcore.SMSPack']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'fleetcore.plan': {
            'Meta': {'object_name': 'Plan'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_min': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'included_sms': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'price_min': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'price_sms': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'with_min_clearing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'with_sms_clearing': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'fleetcore.smspack': {
            'Meta': {'object_name': 'SMSPack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('fleetcore.fields.MoneyField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '3'}),
            'units': ('fleetcore.fields.SMSField', [], {'default': '0'})
        }
    }

    complete_apps = ['fleetcore']